# Swakopmund Municipality Microservices

This repository contains two microservices for the Swakopmund Municipality website:

1. Activities Service
2. Property & Land Management Service

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Activities Service

1. Navigate to the activities service directory:
```bash
cd activities_service
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the service:
### Property & Land Management Service

#### Run Locally (Python)

1. Navigate to the property management service directory:
```bash
cd property_management_service
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the service:
```bash
python main.py
```

The service will be available at `http://localhost:8001`

#### Run with Docker

1. Build the Docker image:
```sh
docker build -t property-management-service .
```

2. Run the Docker container:
```sh
docker run -d -p 8001:8001 --env-file .env property-management-service
```

The service will be available at `http://localhost:8001`

## API Documentation

Once the service is running, you can access its API documentation at:

- Property & Land Management Service: `http://localhost:8001/docs`

## Features

### Activities Service
- Get list of activities with sorting and pagination
- Get detailed information about specific activities

### Property & Land Management Service
- Get property details
- Get property valuation information
- Submit permit applications
- Check permit application status

## Note
This is a development version with mock data. In a production environment, you would need to:
1. Set up a proper database
2. Implement authentication and authorization
3. Add input validation
4. Set up proper error handling
5. Configure CORS
6. Add logging
7. Set up monitoring and health checks 