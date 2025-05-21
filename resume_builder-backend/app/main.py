from fastapi import FastAPI
from app.routers import ai_router # Importing the new AI router
# Assuming other routers might exist as per the task description example
# from app.routers import auth_router, resume_router

app = FastAPI(
    title="Resume Builder API",
    description="API for managing resumes and providing AI-powered suggestions.",
    version="0.1.0"
)

# Include existing routers if they were present (based on task example)
# app.include_router(auth_router.router, prefix="/api/auth", tags=["Authentication"])
# app.include_router(resume_router.router, prefix="/api/resumes", tags=["Resumes"])

# Include the new AI router
app.include_router(ai_router.router, prefix="/api/ai", tags=["AI Suggestions"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Resume Builder API!"}
