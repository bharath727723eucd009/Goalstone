"""Main FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from observability.logger import configure_logging
from observability.middleware import LoggingMetricsMiddleware
from config import settings
import structlog

# Configure logging
configure_logging()
logger = structlog.get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Life Goal Management System",
    description="Multi-agent system for personalized life goal management",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

# Include agent routes
from api.agent_routes import router as agent_router
app.include_router(agent_router, prefix="/api/v1")

# Include auth routes
from auth.routes import router as auth_router
app.include_router(auth_router, prefix="/api/v1")

# Include data routes
from api.data_routes import router as data_router
app.include_router(data_router, prefix="/api/v1")

# Add middlewares
from auth.middleware import AuthMiddleware
from sessions.session_manager import InMemorySessionManager

session_manager = InMemorySessionManager()
app.add_middleware(LoggingMetricsMiddleware)
app.add_middleware(AuthMiddleware, session_manager=session_manager)

# Include metrics routes
from api.metrics_routes import router as metrics_router
app.include_router(metrics_router)

@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("Starting AI Life Goal Management System")
    
    # Connect to MongoDB
    from database.connection import connect_to_mongo
    await connect_to_mongo()
    
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Shutting down AI Life Goal Management System")
    
    # Close MongoDB connection
    from database.connection import close_mongo_connection
    await close_mongo_connection()

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Life Goal Management System",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )