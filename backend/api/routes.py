from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from ..models.traffic import TrafficData, ServiceConnection
from ..core.processor import TrafficProcessor
from ..core.ingestion import DataIngestionService
from datetime import datetime

router = APIRouter()
processor = TrafficProcessor()
ingestion_service = DataIngestionService()

@router.post("/traffic/batch", response_model=Dict)
async def ingest_traffic_batch(traffic_batch: List[TrafficData]):
    """Ingest batch traffic data"""
    try:
        if not traffic_batch:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Traffic batch cannot be empty"
            )
        await ingestion_service.ingest_traffic_batch(traffic_batch)
        return {
            "status": "success",
            "message": f"Ingested {len(traffic_batch)} traffic records",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest traffic batch: {str(e)}"
        )

@router.post("/traffic", response_model=Dict)
async def ingest_traffic(traffic: TrafficData):
    """Ingest traffic data"""
    try:
        await ingestion_service.ingest_traffic(traffic)
        return {
            "status": "success",
            "message": "Traffic data ingested",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest traffic data: {str(e)}"
        )

@router.post("/service-registry", response_model=Dict)
async def update_service_registry(registry: Dict[str, str]):
    """Update service registry"""
    try:
        if not registry:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service registry cannot be empty"
            )
        await ingestion_service.update_service_registry(registry)
        return {
            "status": "success",
            "message": "Service registry updated",
            "services": len(registry)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update service registry: {str(e)}"
        )

@router.get("/service-map", response_model=List[ServiceConnection])
async def get_service_map(min_score: float = 0.1):
    """Get current service map"""
    try:
        traffic_data = await ingestion_service.get_recent_traffic()
        service_registry = await ingestion_service.get_service_registry()
        
        if not service_registry:
            return []  # Return empty list instead of error when no services registered
            
        connections = processor.scoring_engine.calculate_score(
            traffic_data,
            service_registry
        )
        
        filtered_connections = [
            conn for conn in connections 
            if conn.score >= min_score
        ]
        
        return filtered_connections
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate service map: {str(e)}"
        )