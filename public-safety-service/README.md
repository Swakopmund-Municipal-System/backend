# Swakopmund Municipality Public Safety Service

A comprehensive REST API service for managing fire, law enforcement, and emergency response incidents in Swakopmund Municipality.

## 🚀 Features

- **Incident Reporting**: Report fire and emergency incidents
- **Status Management**: Update and track incident status
- **User Management**: Support for residents, fire department, and law enforcement
- **RESTful API**: Clean, well-documented REST endpoints
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Docker Support**: Containerized deployment
- **API Documentation**: Auto-generated OpenAPI/Swagger docs
- **Health Monitoring**: Built-in health checks
- **Logging**: Comprehensive application logging

## 🏗️ Architecture

The application follows clean architecture principles:

```
app/
├── api/                    # API layer
│   └── v1/
│       ├── endpoints/      # API endpoints
│       └── api.py         # API router configuration
├── core/                   # Core functionality
│   ├── config.py          # Configuration management
│   └── database.py        # Database connection
├── models/                 # Database models
│   └── incident.py        # Incident model
├── schemas/                # Pydantic schemas
│   └── incident.py        # Request/response schemas
├── services/               # Business logic
│   └── incident_service.py # Incident management service
└── main.py                # Application entry point
```

## 📊 Database Schema

### PublicSafetyIncidentReports
| Column      | Type         | Description                    |
|-------------|--------------|--------------------------------|
| id          | INT (PK)     | Primary key                    |
| description | TEXT         | Incident description           |
| date        | DATE         | Incident date                  |
| location    | VARCHAR(255) | General location               |
| address     | VARCHAR(255) | Specific address               |
| status      | VARCHAR(50)  | Current status                 |
| user_id     | INT (FK)     | Reporting user ID              |
| created_at  | DATETIME     | Record creation timestamp      |
| updated_at  | DATETIME     | Record update timestamp        |

## 🔗 API Endpoints

### Fire Department Endpoints

| Method | Endpoint                    | Description                |
|--------|-----------------------------|----------------------------|
| POST   | `/api/v1/fire/report-incident` | Report a new fire incident |
| POST   | `/api/v1/fire/status`       | Update incident status     |
| GET    | `/api/v1/fire/incident/{id}` | Get incident details       |
| GET    | `/api/v1/fire/incidents`    | List incidents (paginated) |

### System Endpoints

| Method | Endpoint                | Description        |
|--------|-------------------------|--------------------|
| GET    | `/`                     | Root endpoint      |
| GET    | `/api/v1/health`        | Health check       |
| GET    | `/api/docs`             | API documentation  |

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ASD-Public-Safety-Service
```

### 2. Environment Setup

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your configuration
nano .env
```

### 3. Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Access the Services

- **API Documentation**: http://localhost:8686/api/docs
- **Public Safety Service**: http://localhost:8686
- **PostgreSQL**: localhost:5432
- **pgAdmin**: http://localhost:5050 (admin@swakopmund.gov.na / admin123)

## 🛠️ Development Setup

### Local Development

1. **Install Python 3.11+**

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Environment Variables**
```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/public_safety_db"
export DEBUG=true
```

5. **Run PostgreSQL**
```bash
docker run -d \
  --name postgres-dev \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=public_safety_db \
  -p 5432:5432 \
  postgres:15-alpine
```

6. **Start Development Server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8686
```

## 📝 API Usage Examples

### Report a Fire Incident

```bash
curl -X POST "http://localhost:8686/api/v1/fire/report-incident" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "location": "Swakopmund City Center",
    "address": "123 Main Street, Swakopmund",
    "description": "Fire reported in commercial building, smoke visible from second floor"
  }'
```

### Update Incident Status

```bash
curl -X POST "http://localhost:8686/api/v1/fire/status?incident_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "IN_PROGRESS"
  }'
```

### Get Incident Details

```bash
curl -X GET "http://localhost:8686/api/v1/fire/incident/1"
```

### List All Incidents

```bash
curl -X GET "http://localhost:8686/api/v1/fire/incidents?page=1&size=10"
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_incident_service.py
```

## 📋 Production Deployment

### 1. Environment Configuration

Update the `.env` file for production:

```env
DEBUG=false
SECRET_KEY=your-super-secure-secret-key
DATABASE_URL=postgresql://user:password@your-db-host:5432/production_db
LOG_LEVEL=WARNING
```

### 2. Database Setup

```bash
# Create production database
createdb public_safety_production

# Run migrations (if using Alembic)
alembic upgrade head
```

### 3. Deploy with Docker

```bash
# Build production image
docker build -t public-safety-service:latest .

# Run with production configuration
docker-compose -f docker-compose.prod.yml up -d
```

## 🔒 Security Considerations

- Change default passwords in production
- Use environment variables for sensitive data
- Implement proper authentication/authorization
- Enable HTTPS in production
- Configure firewall rules
- Regular security updates

## 📊 Monitoring and Logging

The application includes:

- Health check endpoints
- Structured logging
- Request/response timing
- Error tracking
- Database connection monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:

- **Email**: support@swakopmund.gov.na
- **Phone**: +264 64 4104 2000
- **Address**: Swakopmund Municipality, Namibia

## 🏛️ About Swakopmund Municipality

Swakopmund Municipality is committed to providing efficient and reliable public safety services to our community. This digital platform enhances our emergency response capabilities and ensures better coordination between residents and emergency services.

---

**Swakopmund Municipality Public Safety Service** - Serving our community with technology and dedication. 