# Service Map Visualization

A real-time service dependency visualization tool that helps SREs understand relationships between various services in a Kubernetes environment. The application processes network traffic data and service registry information to create an interactive service map.

## Features

- Basic service relationship visualization using D3
- Simple relationship scoring based on traffic volume
- Adjustable minimum score filtering using a slider
- Automatic updates every 30 seconds
- Support for multiple service connections
- Basic error handling and loading states
- Draggable nodes and zoomable interface

## Requirements
- Python 3.8-3.11

## Architecture

The project consists of two main components:

### Backend (Python/FastAPI)
- Traffic data ingestion
- Service registry management
- Relationship scoring algorithm
- RESTful API endpoints

### Frontend (React/TypeScript)
- Interactive D3 visualization
- Real-time data polling
- Score-based filtering
- Error and loading state management

## Prerequisites

- Python 3.10+
- Node.js 16+
- npm 8+

## Installation

### Backend Setup
```bash
# Clone the repository
git clone <repository-url>
cd service_map

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Unix/MacOS
# or
.\venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## Running the Application

1. Start the backend server:
```bash
# From the service_map directory
uvicorn backend.main:app --reload --port 8000
```

2. Start the frontend development server:
```bash
# From the frontend directory
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## API Endpoints

### Service Registry
```bash
# Update service registry
curl -X POST http://localhost:8000/api/v1/service-registry -H "Content-Type: application/json" -d '{
  "10.128.72.69": "Login Service",
  "10.128.72.20": "Auth",
  "10.128.72.14": "Gaming UI",
  "10.128.24.14": "User Profile DB",
  "10.128.72.12": "Gaming Service"
}'
```

### Traffic Data
```bash
# Send traffic data
curl -X POST http://localhost:8000/api/v1/traffic -H "Content-Type: application/json" -d '{
  "source_ip": "10.128.72.69",
  "source_port": 32032,
  "dest_ip": "10.128.72.20",
  "dest_port": 443,
  "timestamp": "2024-02-01T12:00:00Z"
}'

# Send batch traffic data
curl -X POST http://localhost:8000/api/v1/traffic/batch -H "Content-Type: application/json" -d '[
  {
    "source_ip": "10.128.72.69",
    "source_port": 32032,
    "dest_ip": "10.128.72.20",
    "dest_port": 443,
    "timestamp": "2024-02-01T12:00:00Z"
  }
]'
```


## Testing

### Backend Tests
```bash
# Run Python tests
pytest -v
```

### Frontend Tests
```bash
# Run React tests
npm test

# Run with coverage
npm run test:coverage
```

## Future Enhancements

### 1. Intelligent Relationship Scoring
Currently, the service implements basic scoring based on traffic volume. Future improvements will include:
- Weighted scoring algorithm considering multiple factors:
  - Traffic frequency and patterns
  - Time-of-day patterns
  - Request latency patterns
  - Common request paths (like Auth → DB → Service)
- Service relationship confidence scoring
- Critical path identification
- Traffic pattern analysis over time
- Service dependency weight calculations

### 2. Enhanced Interactive Visualization
The current visualization provides basic service mapping. Planned enhancements include:
- Service "heat" visualization based on traffic volume
- Time-based playback of traffic patterns
- Advanced filtering and highlighting of paths
- Detailed metrics display on hover
- Custom view layouts for different analysis needs
- Path analysis tools
- Service cluster visualization
- Historical trend visualization
- Custom node grouping and organization
- Export and sharing capabilities

### 3. Anomaly Detection System
Future implementation will include a comprehensive anomaly detection system:
- Detection of unusual traffic patterns
- Service degradation identification
- Unauthorized connection flagging
- Historical pattern analysis
- Real-time alerts for:
  - Sudden changes in traffic patterns
  - Unusual service connections
  - Service response time anomalies
  - Failed connection attempts
- Machine learning-based pattern recognition
- Customizable alert thresholds
- Anomaly visualization in the service map