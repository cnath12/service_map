from typing import Dict, List, Optional
from datetime import datetime
from ..models.traffic import TrafficData
import asyncio
from collections import deque

class DataIngestionService:
    def __init__(self):
        self.traffic_buffer = deque(maxlen=1000)  # Rolling buffer of last 1000 events
        self.service_registry: Dict[str, str] = {}  # IP to service name mapping
        self._lock = asyncio.Lock()
        
    async def ingest_traffic(self, traffic: TrafficData) -> None:
        """Ingest a single traffic event"""
        async with self._lock:
            self.traffic_buffer.append(traffic)
    
    async def ingest_traffic_batch(self, traffic_batch: List[TrafficData]) -> None:
        """Ingest multiple traffic events"""
        async with self._lock:
            for traffic in traffic_batch:
                self.traffic_buffer.append(traffic)
    
    async def update_service_registry(self, registry: Dict[str, str]) -> None:
        """Update the service registry mapping"""
        async with self._lock:
            self.service_registry = registry
    
    async def get_recent_traffic(self, limit: Optional[int] = None) -> List[TrafficData]:
        """Get recent traffic data"""
        async with self._lock:
            if limit:
                return list(self.traffic_buffer)[-limit:]
            return list(self.traffic_buffer)
    
    async def get_service_registry(self) -> Dict[str, str]:
        """Get current service registry"""
        async with self._lock:
            return self.service_registry.copy()
    
    async def clear_old_data(self, threshold: datetime) -> None:
        """Clear data older than threshold"""
        async with self._lock:
            self.traffic_buffer = deque(
                [t for t in self.traffic_buffer if t.timestamp >= threshold],
                maxlen=self.traffic_buffer.maxlen
            )