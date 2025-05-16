// server.js
const express = require('express');
const puppeteer = require('puppeteer');
const handlebars = require('handlebars');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

// 中间件，用于解析JSON请求体
app.use(express.json());

// 编译Handlebars模板的函数
async function compileTemplate(templateName, data) {
    const filePath = path.join(__dirname, 'templates', `${templateName}.hbs`);
    const htmlContent = await fs.promises.readFile(filePath, 'utf-8');
    return handlebars.compile(htmlContent)(data);
}

// API端点：生成简历PDF
app.post('/generate-resume', async (req, res) => {
    try {
        // 1. 获取用户数据 (目前我们先用固定的示例数据)
        const resumeData = req.body.resumeData || { // 允许通过请求体传递数据，否则使用默认
            personalInfo: {
                name: "张三",
                email: "zhangsan@example.com",
                phone: "13800138000"
            },
            education: [
                { school: "北京大学", degree: "学士", major: "计算机科学", startDate: "2018-09", endDate: "2022-06" },
                { school: "清华大学", degree: "硕士", major: "人工智能", startDate: "2022-09", endDate: "2025-06" }
            ],
            experience: [
                {
                    company: "ABC科技有限公司",
                    position: "软件工程师实习生",
                    startDate: "2024-07",
                    endDate: "2024-12",
                    responsibilities: [
                        "参与需求分析和系统设计。",
                        "编写高质量的代码并进行单元测试。",
                        "协助解决技术难题。"
                    ]
                }
            ],
            skills: ["JavaScript", "Node.js", "React", "数据库管理"]
        };

        // 2. 编译HTML模板
        const htmlContent = await compileTemplate('basic-resume', resumeData);

        // 3. 使用Puppeteer生成PDF
        const browser = await puppeteer.launch({
            headless: "new", // 使用新的无头模式
            args: ['--no-sandbox', '--disable-setuid-sandbox'] // 在某些环境下需要
        });
        const page = await browser.newPage();
        await page.setContent(htmlContent, { waitUntil: 'networkidle0' }); // 等待网络空闲
        const pdfBuffer = await page.pdf({
            format: 'A4',
            printBackground: true, // 打印背景
            margin: { // 设置边距
                top: '20mm',
                right: '20mm',
                bottom: '20mm',
                left: '20mm'
            }
        });
        await browser.close();

        // 4. 发送PDF给客户端
        res.set({
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment; filename=resume.pdf', // 提示浏览器下载
            'Content-Length': pdfBuffer.length
        });
        res.send(pdfBuffer);

    } catch (error) {
        console.error('Error generating PDF:', error);
        res.status(500).send('生成PDF时出错: ' + error.message);
    }
});

app.listen(port, () => {
    console.log(`简历生成器后端服务运行在 http://localhost:${port}`);
});