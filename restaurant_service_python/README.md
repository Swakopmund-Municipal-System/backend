# Restaurant Service

This service manages restaurant information and reviews for the Swakopmund project. It provides endpoints for fetching restaurant details and managing reviews.

## Features

- Fetch restaurant listings with filtering options
- Get featured restaurants
- Add and manage restaurant reviews
- Full integration with the authentication service
- PostgreSQL database for data persistence

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
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
   docker-compose up --build
   ```

### Manual Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the startup script:
   ```bash
   ./startup.sh
   ```

## API Endpoints

### Authentication

All endpoints require the following headers:
- `x-api-key`: Your application's API key
- `x-resource`: "restaurants"
- `x-sub-resource`: Either "fetch-restaurants" or "review-restaurants"
- `Authorization`: "Token <user_token>" (required for authenticated endpoints)

### Available Endpoints

1. Get All Restaurants (Anonymous)
   ```http
   GET /api/restaurants/
   Query Parameters:
   - name (optional): Filter by restaurant name
   - cuisine (optional): Filter by cuisine type
   - price_range (optional): Filter by price range
   - is_featured (optional): Filter featured restaurants
   ```

2. Get Featured Restaurants (Anonymous)
   ```http
   GET /api/restaurants/featured
   ```

3. Get Restaurant Details (Anonymous)
   ```http
   GET /api/restaurants/{restaurant_id}
   ```

4. Add Restaurant Review (Authenticated)
   ```http
   POST /api/restaurants/{restaurant_id}/reviews
   Body:
   {
     "user_id": int,
     "rating": float,
     "comment": string
   }
   ```

## Database Schema

The service uses two main tables:

1. `restaurants`:
   - id (Primary Key)
   - name
   - description
   - address
   - phone
   - website
   - cuisine
   - price_range
   - hours
   - latitude
   - longitude
   - image_url
   - is_featured
   - rating

2. `reviews`:
   - id (Primary Key)
   - restaurant_id (Foreign Key)
   - user_id
   - rating
   - comment
   - created_at

## Error Handling

The service returns appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

## Contributing

1. Ensure you have the required permissions from the authentication service
2. Follow the project's coding standards
3. Test your changes thoroughly
4. Update documentation as needed 