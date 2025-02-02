from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class TrafficData(BaseModel):
    source_ip: str
    source_port: int
    dest_ip: str
    dest_port: int
    timestamp: datetime
    metadata: Optional[Dict] = {}

class ServiceConnection(BaseModel):
    source_service: str
    target_service: str
    score: float
    traffic_count: int