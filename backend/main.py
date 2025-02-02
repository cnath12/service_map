from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import routes
from .core.ingestion import DataIngestionService
from .core.processor import TrafficProcessor

app = FastAPI(title="Service Map API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ingestion_service = DataIngestionService()
traffic_processor = TrafficProcessor()

# Include routers
app.include_router(routes.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # Initialize services, connections etc.
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Cleanup resources
    pass