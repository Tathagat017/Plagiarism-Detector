"""
Main FastAPI application for the Plagiarism Detector backend.
"""

import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import uvicorn

from app.config import settings
from app.api.analyze import router as analyze_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Plagiarism Detector API",
    description="Semantic similarity analyzer for plagiarism detection using sentence embeddings",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
    
    return response

# Include API routes
app.include_router(
    analyze_router,
    prefix="/api/v1",
    tags=["Analysis"]
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Plagiarism Detector API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
        "models": "/api/v1/models"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred",
            "error": str(exc) if settings.DEBUG else "Internal server error"
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("Starting Plagiarism Detector API...")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Available models: {settings.get_available_models()}")
    logger.info(f"Default model: {settings.DEFAULT_MODEL}")
    logger.info(f"Default threshold: {settings.SIMILARITY_THRESHOLD}")
    logger.info("API startup completed")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("Shutting down Plagiarism Detector API...")
    # Clean up resources if needed
    from app.services.embeddings import embedding_service
    embedding_service.clear_all_models()
    logger.info("API shutdown completed")

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    ) 