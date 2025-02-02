import pytest
from fastapi.testclient import TestClient
from datetime import datetime

def test_update_service_registry(test_client, sample_service_registry):
    response = test_client.post(
        "/api/v1/service-registry",
        json=sample_service_registry
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["services"] == len(sample_service_registry)

def test_ingest_traffic_batch(test_client, sample_traffic_data):
    response = test_client.post(
        "/api/v1/traffic/batch",
        json=sample_traffic_data
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == f"Ingested {len(sample_traffic_data)} traffic records"

def test_get_service_map_empty(test_client):
    response = test_client.get("/api/v1/service-map")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_service_map_with_data(test_client, sample_service_registry, sample_traffic_data):
    # First register services
    test_client.post("/api/v1/service-registry", json=sample_service_registry)
    
    # Then send traffic data
    test_client.post("/api/v1/traffic/batch", json=sample_traffic_data)
    
    # Get service map
    response = test_client.get("/api/v1/service-map")
    assert response.status_code == 200
    service_map = response.json()
    assert len(service_map) > 0
    
    # Verify connection structure
    connection = service_map[0]
    assert "source_service" in connection
    assert "target_service" in connection
    assert "score" in connection
    assert isinstance(connection["score"], float)

@pytest.mark.parametrize("min_score", [0.1, 0.5, 0.9])
def test_service_map_filtering(test_client, sample_service_registry, sample_traffic_data, min_score):
    # Setup data
    test_client.post("/api/v1/service-registry", json=sample_service_registry)
    test_client.post("/api/v1/traffic/batch", json=sample_traffic_data)
    
    # Test filtering
    response = test_client.get(f"/api/v1/service-map?min_score={min_score}")
    assert response.status_code == 200
    service_map = response.json()
    
    # Verify all connections meet minimum score
    for connection in service_map:
        assert connection["score"] >= min_score