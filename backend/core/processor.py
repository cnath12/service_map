from typing import List, Dict
from ..models.traffic import TrafficData
from .scoring import RelationshipScoring

class TrafficProcessor:
    def __init__(self):
        self.scoring_engine = RelationshipScoring()
        self.traffic_buffer: List[TrafficData] = []
        self.buffer_size = 1000
        
    async def process_traffic(self, traffic: TrafficData, service_registry: Dict):
        self.traffic_buffer.append(traffic)
        
        if len(self.traffic_buffer) >= self.buffer_size:
            connections = self.scoring_engine.calculate_score(
                self.traffic_buffer, 
                service_registry
            )
            self.traffic_buffer = []
            return connections
        
        return None