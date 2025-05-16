// server.js (부분 수정 및 추가)
const express = require('express');
const puppeteer = require('puppeteer');
const handlebars = require('handlebars');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/templates', express.static(path.join(__dirname, 'templates')));

// NEW: Serve templates statically IF you want them client-accessible for advanced preview
// For now, only backend needs them, but this might be useful later.
// app.use('/templates', express.static(path.join(__dirname, 'templates')));


// List of available templates (filename without .hbs extension)
const AVAILABLE_TEMPLATES = ['basic-resume', 'modern-resume'];

async function compileTemplate(templateName, data) {
    // Security check: Ensure the templateName is valid and prevent directory traversal
    if (!AVAILABLE_TEMPLATES.includes(templateName)) {
        throw new Error(`Template "${templateName}" is not available.`);
    }
    const filePath = path.join(__dirname, 'templates', `${templateName}.hbs`);
    try {
        const htmlFileContent = await fs.promises.readFile(filePath, 'utf-8');
        return handlebars.compile(htmlFileContent)(data);
    } catch (readError) {
        console.error(`Error reading template file: ${filePath}`, readError);
        throw new Error(`Could not read template file: ${templateName}.hbs`);
    }
}

app.post('/generate-resume', async (req, res) => {
    try {
        const resumeData = req.body.resumeData; // Expect structured data
        const templateName = req.body.templateName || 'basic-resume'; // Default to basic-resume

        if (!resumeData) {
            return res.status(400).send('Resume data is missing.');
        }

        const htmlContent = await compileTemplate(templateName, resumeData);

        const browser = await puppeteer.launch({
            headless: "new",
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();
        await page.setContent(htmlContent, { waitUntil: 'networkidle0' });
        const pdfBuffer = await page.pdf({
            format: 'A4',
            printBackground: true,
            margin: { top: '20mm', right: '20mm', bottom: '20mm', left: '20mm' }
        });
        await browser.close();

        res.set({
            'Content-Type': 'application/pdf',
            'Content-Disposition': `attachment; filename="${templateName}-${Date.now()}.pdf"`,
            'Content-Length': pdfBuffer.length
        });
        res.send(pdfBuffer);

    } catch (error) {
        console.error('Error generating PDF:', error);
        res.status(500).send('Error generating PDF: ' + error.message);
    }
});

// Optional: Endpoint to list available templates for the frontend
app.get('/api/templates', (req, res) => {
    res.json(AVAILABLE_TEMPLATES.map(name => ({ id: name, displayName: name.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase()) })));
});


app.listen(port, () => {
    console.log(`Resume builder backend running on http://localhost:${port}`);
    console.log(`Frontend available at: http://localhost:${port}/`);
});