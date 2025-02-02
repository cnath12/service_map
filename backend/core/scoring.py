from typing import Dict, List
from ..models.traffic import TrafficData, ServiceConnection

class RelationshipScoring:
    def __init__(self):
        self.traffic_threshold = 1  # Changed from 10 to 1 for testing
        
    def calculate_score(self, traffic_data: List[TrafficData], service_registry: Dict) -> List[ServiceConnection]:
        # Group traffic by service pairs
        service_pairs: Dict[tuple, int] = {}
        
        for traffic in traffic_data:
            source_service = self._get_service_name(traffic.source_ip, service_registry)
            target_service = self._get_service_name(traffic.dest_ip, service_registry)
            
            if source_service and target_service:
                pair = (source_service, target_service)
                service_pairs[pair] = service_pairs.get(pair, 0) + 1
        
        # Calculate scores
        connections = []
        max_traffic = max(service_pairs.values()) if service_pairs else 1
        
        for (source, target), traffic_count in service_pairs.items():
            if traffic_count >= self.traffic_threshold:
                score = self._normalize_score(traffic_count, max_traffic)
                connections.append(ServiceConnection(
                    source_service=source,
                    target_service=target,
                    score=score,
                    traffic_count=traffic_count
                ))
        
        return connections
    
    def _normalize_score(self, traffic_count: int, max_traffic: int) -> float:
        return min(1.0, traffic_count / max_traffic)
    
    def _get_service_name(self, ip: str, service_registry: Dict) -> str:
        return service_registry.get(ip)