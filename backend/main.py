"""Main FastAPI application for dental diagnosis."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import ALLOWED_ORIGINS
from app.routes.diagnosis import router as diagnosis_router

# Create FastAPI app
app = FastAPI(
    title="Dental Diagnosis API",
    description="AI-powered dental X-ray analysis for cavity and gum disease detection",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(diagnosis_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Dental Diagnosis API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
