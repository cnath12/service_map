import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..core.ingestion import DataIngestionService
from ..core.processor import TrafficProcessor

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def sample_service_registry():
    return {
        "10.128.72.69": "Login Service",
        "10.128.72.20": "Auth",
        "10.128.72.14": "Gaming UI",
        "10.128.24.14": "User Profile DB",
        "10.128.72.12": "Gaming Service"
    }

@pytest.fixture
def sample_traffic_data():
    return [
        {
            "source_ip": "10.128.72.69",
            "source_port": 32032,
            "dest_ip": "10.128.72.20",
            "dest_port": 443,
            "timestamp": "2024-02-01T12:00:00Z"
        },
        {
            "source_ip": "10.128.72.20",
            "source_port": 27892,
            "dest_ip": "10.128.24.14",
            "dest_port": 5432,
            "timestamp": "2024-02-01T12:00:01Z"
        }
    ]

@pytest.fixture
def ingestion_service():
    return DataIngestionService()

@pytest.fixture
def processor():
    return TrafficProcessor()