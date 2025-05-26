# Restaurant Service

This service manages restaurant information and reviews for the Swakopmund project. It provides endpoints for fetching restaurant details and managing reviews.

## Features

- Fetch restaurant listings with filtering options
- Get featured restaurants
- Get detailed restaurant information
- Add and manage restaurant reviews
- PostgreSQL database for data persistence

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- API key from the system administrator

## Environment Variables

Create a `.env` file based on `example.env` with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:postgres@restaurant-db:5432/restaurant_db

# Authentication Service Configuration
AUTH_SERVICE_URL=http://auth-service:8000

# Service Configuration
PORT=8002
HOST=0.0.0.0
```

## Running the Service

### Using Docker Compose

1. Ensure you're in the service directory:
   ```bash
   cd restaurant_service_python
   ```

2. Start the service:
   ```bash
   docker compose up --build
   ```

The service will be available at `http://localhost:8002`

## API Documentation

Once the service is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8002/docs`
- ReDoc: `http://localhost:8002/redoc`

## API Endpoints

### Required Headers

For all endpoints, you need to provide:
- `x-api-key`: Your application's API key
- `x-resource`: "restaurants"

For authenticated endpoints (like adding reviews), you also need:
- `Authorization`: Bearer token from the authentication service

### Available Endpoints

1. Get All Restaurants
   ```http
   GET /
   Headers:
   - x-api-key: your-api-key
   - x-resource: restaurants
   
   Query Parameters:
   - name (optional): Filter by restaurant name
   - cuisine (optional): Filter by cuisine type
   - price_range (optional): Filter by price range
   - is_featured (optional): Filter featured restaurants
   ```

2. Get Featured Restaurants
   ```http
   GET /featured
   Headers:
   - x-api-key: your-api-key
   - x-resource: restaurants
   ```

3. Get Restaurant Details
   ```http
   GET /{restaurant_id}
   Headers:
   - x-api-key: your-api-key
   - x-resource: restaurants
   ```

4. Create Restaurant
   ```http
   POST /
   Headers:
   - x-api-key: your-api-key
   - x-resource: restaurants
   
   Body:
   {
     "name": "string",
     "description": "string",
     "address": "string",
     "phone": "string (optional)",
     "website": "string (optional)",
     "cuisine": "string (optional)",
     "price_range": "string (optional)",
     "hours": "string (optional)",
     "latitude": "float (optional)",
     "longitude": "float (optional)",
     "image_url": "string (optional)",
     "is_featured": "boolean (default: false)",
     "rating": "float (default: 0.0)"
   }
   ```

5. Add Restaurant Review
   ```http
   POST /{restaurant_id}/reviews
   Headers:
   - x-api-key: your-api-key
   - x-resource: restaurants
   - Authorization: Bearer your-token
   
   Body:
   {
     "user_id": "integer",
     "rating": "float",
     "comment": "string"
   }
   ```

## Data Models

### Restaurant
```python
{
    "id": "integer",
    "name": "string",
    "description": "string",
    "address": "string",
    "phone": "string (optional)",
    "website": "string (optional)",
    "cuisine": "string (optional)",
    "price_range": "string (optional)",
    "hours": "string (optional)",
    "latitude": "float (optional)",
    "longitude": "float (optional)",
    "image_url": "string (optional)",
    "is_featured": "boolean",
    "rating": "float",
    "reviews": "array of Review objects"
}
```

### Review
```python
{
    "id": "integer",
    "restaurant_id": "integer",
    "user_id": "integer",
    "rating": "float",
    "comment": "string",
    "created_at": "datetime"
}
```

## Error Handling

The service returns appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized (missing or invalid headers)
- 404: Not Found
- 500: Internal Server Error

## Development

### Local Development Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the service:
   ```bash
   uvicorn main:app --reload --port 8002
   ```

### Testing

The service includes comprehensive logging. You can monitor the logs using:
```bash
docker compose logs -f restaurant-service
```

## Contributing

1. Follow the project's coding standards
2. Ensure all endpoints are properly documented
3. Test your changes thoroughly
4. Update this documentation as needed 