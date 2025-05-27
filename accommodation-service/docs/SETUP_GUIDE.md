# Accommodation API Service - Setup Guide

## Project Structure
```
ASD-Accommodation-Service/
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py           # Database configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── accommodation.py      # SQLAlchemy models
│   │   └── schemas.py           # Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   └── accommodation_service.py  # Business logic
│   ├── routers/
│   │   ├── __init__.py
│   │   └── accommodations.py    # API routes
│   └── main.py                  # FastAPI application
├── scripts/
│   ├── simple_server.py         # HTTP server implementation
│   └── seed_data.py            # Database seeding script
├── tests/
│   └── test_api.py             # API tests
├── docs/
│   ├── API_SPECIFICATION.md    # API documentation
│   └── SETUP_GUIDE.md          # This file
├── docker-compose.yml          # Docker compose configuration
├── Dockerfile                  # Docker container configuration
├── requirements.txt            # Python dependencies
├── README.md                   # Project overview
└── accommodation.db            # SQLite database file
```

## Prerequisites

- Python 3.9 or higher (Note: Python 3.13 has compatibility issues with some packages)
- pip (Python package installer)
- Git (for version control)
- Optional: Docker and Docker Compose

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ASD-Accommodation-Service
```

### 2. Create Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
Run the database seeding script to create tables and populate with sample data:
```bash
python scripts/seed_data.py
```

You should see output like:
```
🌱 Seeding database with sample accommodation data...
============================================================
✅ Database tables created/verified
✅ Successfully created 3 accommodations with images and reviews!
```

### 5. Test the Setup
Run the test script to verify everything is working:
```bash
python tests/test_api.py
```

Expected output:
```
🧪 Testing Accommodation API
==================================================
✅ Database connection works! Found 3 accommodations.
🔍 Testing GET /api/accommodations/
✅ Found 3 accommodations
...
✅ All tests passed! The API should work correctly.
```

## Running the Service

### Option 1: Using the Simple HTTP Server (Recommended)
The project includes a custom HTTP server that works reliably:

```bash
python scripts/simple_server.py
```

The server will start on `http://localhost:8585` with output:
```
🚀 Accommodation API Server starting on http://localhost:8585
📋 Available endpoints:
   GET  http://localhost:8585/api/accommodations/
   GET  http://localhost:8585/api/accommodations/{id}
   POST http://localhost:8585/api/accommodations/{id}/reviews
```

### Option 2: Using FastAPI/Uvicorn (May have compatibility issues)
If you have compatible package versions:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8585 --reload
```

### Option 3: Using Docker
Make sure Docker is running, then:
```bash
# Quick start
docker compose up -d

# Or use the Docker manager for full deployment
python scripts/docker_manager.py deploy

# Check status
python scripts/docker_manager.py status

# Test the API
python scripts/docker_manager.py test
```

The Docker deployment includes:
- Automatic database creation and seeding
- Health monitoring
- Easy container management via docker_manager.py script

## Testing the API

### Using curl
```bash
# Get all accommodations
curl -X GET "http://localhost:8585/api/accommodations/"

# Get specific accommodation
curl -X GET "http://localhost:8585/api/accommodations/1"

# Add a review
curl -X POST "http://localhost:8585/api/accommodations/1/reviews" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 123, "rating": 4.5, "comment": "Great place!"}'
```

### Using Browser
Open your browser and navigate to:
- http://localhost:8585/api/accommodations/
- http://localhost:8585/api/accommodations/1

## Database

The project uses SQLite for simplicity and compatibility. The database file `accommodation.db` will be created automatically when you run the seeding script.

### Database Schema
- **Accommodation**: Main accommodation information
- **AccommodationImage**: Images associated with accommodations
- **Review**: User reviews for accommodations

### Viewing Database Content
You can use any SQLite browser or command-line tool:
```bash
sqlite3 accommodation.db
.tables
SELECT * FROM accommodation;
```

## Troubleshooting

### Python 3.13 Compatibility Issues
If you encounter ForwardRef or other compatibility errors with Python 3.13:
1. Use Python 3.9-3.12 instead
2. Use the simple_server.py instead of FastAPI
3. The project is designed to work around these compatibility issues

### Port Already in Use
If port 8585 is already in use, you can change the port in:
- `scripts/simple_server.py` (line with `def run_server(port=8585)`)
- `docker-compose.yml`
- `Dockerfile`

### Database Issues
If you encounter database errors:
1. Delete the `accommodation.db` file
2. Run `python scripts/seed_data.py` again

### Package Installation Issues
If pip installation fails:
1. Upgrade pip: `pip install --upgrade pip`
2. Install packages individually
3. Check Python version compatibility

## Development

### Adding New Features
1. Models: Add to `app/models/accommodation.py`
2. Schemas: Add to `app/models/schemas.py`
3. Services: Add business logic to `app/services/accommodation_service.py`
4. Routes: Add endpoints to `app/routers/accommodations.py`
5. Tests: Add tests to `tests/test_api.py`

### Code Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to functions and classes

### Database Migrations
For schema changes:
1. Update models in `app/models/accommodation.py`
2. Delete `accommodation.db`
3. Run `python scripts/seed_data.py`

## Production Deployment

### Environment Variables
Create a `.env` file for production settings:
```
DATABASE_URL=postgresql://user:password@localhost/accommodation_db
SECRET_KEY=your-secret-key
DEBUG=False
```

### Docker Production
Use the provided Dockerfile and docker-compose.yml for containerized deployment.

### Security Considerations
- Add authentication/authorization
- Use HTTPS in production
- Validate and sanitize all inputs
- Use environment variables for sensitive data

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API specification in `docs/API_SPECIFICATION.md`
3. Run the test suite to identify issues
4. Check server logs for error details 