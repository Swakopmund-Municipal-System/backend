# Accommodation API Service

A FastAPI-based microservice providing information about accommodation options in Swakopmund, Namibia.

## Features

- 🏨 Get list of accommodations (with optional name filtering)
- 🔍 Get detailed information about specific accommodations
- ⭐ Add reviews for accommodations
- 🗄️ SQLite database with sample data
- 🐳 Docker containerization support
- 📚 Comprehensive API documentation

## Quick Start

### Prerequisites
- Python 3.9+ (Python 3.13 has compatibility issues - use 3.9-3.12)
- Git

### 1. Clone and Setup
```bash
git clone <repository-url>
cd ASD-Accommodation-Service
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python scripts/seed_data.py
```

### 3. Start Server
```bash
# Simple startup (recommended)
python scripts/simple_server.py

# Or use the advanced startup script
python scripts/start_server.py

# Or with options
python scripts/start_server.py --port 8080 --test
```

The API will be available at http://localhost:8585

## Project Structure

```
ASD-Accommodation-Service/
├── app/                          # Main application package
│   ├── database/                 # Database configuration
│   ├── models/                   # Data models and schemas
│   ├── services/                 # Business logic
│   ├── routers/                  # API route handlers
│   └── main.py                   # FastAPI application
├── scripts/                      # Utility scripts
│   ├── simple_server.py          # HTTP server (Python 3.13 compatible)
│   ├── seed_data.py             # Database seeding
│   └── start_server.py          # Advanced server startup
├── tests/                        # Test files
│   └── test_api.py              # API tests
├── docs/                         # Documentation
│   ├── API_SPECIFICATION.md     # Detailed API docs
│   └── SETUP_GUIDE.md           # Setup instructions
├── docker-compose.yml            # Docker configuration
├── Dockerfile                    # Container definition
├── requirements.txt              # Python dependencies
└── accommodation.db              # SQLite database (auto-created)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accommodations/` | Get list of accommodations |
| GET | `/api/accommodations/{id}` | Get accommodation details |
| POST | `/api/accommodations/{id}/reviews` | Add a review |

### Example Usage

```bash
# Get all accommodations
curl "http://localhost:8585/api/accommodations/"

# Filter by name
curl "http://localhost:8585/api/accommodations/?name=hotel"

# Get specific accommodation
curl "http://localhost:8585/api/accommodations/1"

# Add a review
curl -X POST "http://localhost:8585/api/accommodations/1/reviews" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 123, "rating": 4.5, "comment": "Great place!"}'
```

## Running Options

### Option 1: Simple HTTP Server (Recommended)
Works with all Python versions including 3.13:
```bash
python scripts/simple_server.py
```

### Option 2: Advanced Startup Script
Provides database checks, testing, and fallback options:
```bash
python scripts/start_server.py --help
```

Available options:
- `--port 8080`: Custom port
- `--test`: Run tests before starting
- `--seed`: Force database re-seeding
- `--server simple|fastapi|auto`: Choose server type

### Option 3: FastAPI/Uvicorn
May have compatibility issues with Python 3.13:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8585 --reload
```

### Option 4: Docker
```bash
# Quick start
docker compose up -d

# Or use the Docker manager script
python scripts/docker_manager.py deploy

# Other Docker commands
python scripts/docker_manager.py build   # Build container
python scripts/docker_manager.py start   # Start container
python scripts/docker_manager.py stop    # Stop container
python scripts/docker_manager.py status  # Show status
python scripts/docker_manager.py test    # Test API
python scripts/docker_manager.py logs    # View logs
```

## Testing

```bash
# Run API tests
python tests/test_api.py

# Or use the startup script with testing
python scripts/start_server.py --test

# Test Docker deployment
python scripts/docker_manager.py test
```

## Docker Deployment

The project includes full Docker support for easy deployment:

### Quick Docker Setup
```bash
# Build and start container
docker compose up -d

# Test the API
curl http://localhost:8585/api/accommodations/
```

### Using Docker Manager Script
```bash
# Full deployment (build, start, test)
python scripts/docker_manager.py deploy

# Individual commands
python scripts/docker_manager.py build    # Build the container
python scripts/docker_manager.py start    # Start the container
python scripts/docker_manager.py stop     # Stop the container
python scripts/docker_manager.py restart  # Restart the container
python scripts/docker_manager.py status   # Show container status
python scripts/docker_manager.py test     # Test all API endpoints
python scripts/docker_manager.py logs     # View container logs
python scripts/docker_manager.py cleanup  # Remove containers and images
```

### Docker Features
- ✅ **Auto Database Setup**: Database is created and seeded automatically
- ✅ **Health Checks**: Container monitors API availability
- ✅ **Volume Persistence**: Database persists between container restarts
- ✅ **Port Mapping**: API accessible on localhost:8585
- ✅ **Easy Management**: Use the docker_manager.py script for all operations

## Documentation

- **API Specification**: See `docs/API_SPECIFICATION.md` for detailed endpoint documentation
- **Setup Guide**: See `docs/SETUP_GUIDE.md` for comprehensive setup instructions
- **Live API Docs**: Available at http://localhost:8585/docs (when using FastAPI)

## Database

The service uses SQLite with the following tables:
- **Accommodation**: Main accommodation information
- **AccommodationImage**: Associated images
- **Review**: User reviews and ratings

Sample data includes 3 accommodations in Swakopmund with images and reviews.

## Tech Stack

- **Framework**: FastAPI / Python HTTP Server
- **Database**: SQLite (with SQLAlchemy ORM)
- **Validation**: Pydantic
- **Containerization**: Docker
- **Development**: Python 3.9+

## Troubleshooting

### Python 3.13 Compatibility
If you encounter compatibility issues:
1. Use the simple HTTP server: `python scripts/simple_server.py`
2. Consider downgrading to Python 3.9-3.12
3. Use the provided compatibility scripts

### Port Conflicts
Change the port in:
- `scripts/simple_server.py` 
- `scripts/start_server.py`
- `docker-compose.yml`

### Database Issues
Reset the database:
```bash
rm accommodation.db
python scripts/seed_data.py
```

## Development

### Adding Features
1. Update models in `app/models/`
2. Add business logic in `app/services/`
3. Create API endpoints in `app/routers/`
4. Add tests in `tests/`

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here] 