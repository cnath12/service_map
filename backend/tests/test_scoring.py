import pytest
from datetime import datetime
from ..core.scoring import RelationshipScoring
from ..models.traffic import TrafficData, ServiceConnection

def test_relationship_scoring():
    scoring = RelationshipScoring()
    
    # Test data with multiple traffic entries
    traffic_data = [
        TrafficData(
            source_ip="10.0.0.1",
            source_port=8080,
            dest_ip="10.0.0.2",
            dest_port=443,
            timestamp=datetime.now()
        ),
        # Add another request between same services
        TrafficData(
            source_ip="10.0.0.1",
            source_port=8081,
            dest_ip="10.0.0.2",
            dest_port=443,
            timestamp=datetime.now()
        )
    ]
    
    service_registry = {
        "10.0.0.1": "service-a",
        "10.0.0.2": "service-b"
    }
    
    connections = scoring.calculate_score(traffic_data, service_registry)
    
    # Basic assertions
    assert len(connections) > 0
    assert isinstance(connections[0], ServiceConnection)
    
    # Check specific connection details
    connection = connections[0]
    assert connection.source_service == "service-a"
    assert connection.target_service == "service-b"
    assert connection.traffic_count == 2
    assert connection.score == 1.0  # Should be 1.0 as it's the only connection

def test_missing_service():
    scoring = RelationshipScoring()
    
    traffic_data = [
        TrafficData(
            source_ip="10.0.0.1",
            source_port=8080,
            dest_ip="10.0.0.3",  # IP not in registry
            dest_port=443,
            timestamp=datetime.now()
        )
    ]
    
    service_registry = {
        "10.0.0.1": "service-a",
        "10.0.0.2": "service-b"
    }
    
    connections = scoring.calculate_score(traffic_data, service_registry)
    assert len(connections) == 0  # Should have no connections as one service is missing

def test_multiple_connections():
    scoring = RelationshipScoring()
    
    traffic_data = [
        # Connection A -> B
        TrafficData(
            source_ip="10.0.0.1",
            source_port=8080,
            dest_ip="10.0.0.2",
            dest_port=443,
            timestamp=datetime.now()
        ),
        # Connection B -> C
        TrafficData(
            source_ip="10.0.0.2",
            source_port=8081,
            dest_ip="10.0.0.3",
            dest_port=443,
            timestamp=datetime.now()
        )
    ]
    
    service_registry = {
        "10.0.0.1": "service-a",
        "10.0.0.2": "service-b",
        "10.0.0.3": "service-c"
    }
    
    connections = scoring.calculate_score(traffic_data, service_registry)
    assert len(connections) == 2  # Should have two connections
    
    # Verify all scores are between 0 and 1
    for conn in connections:
        assert 0 <= conn.score <= 1