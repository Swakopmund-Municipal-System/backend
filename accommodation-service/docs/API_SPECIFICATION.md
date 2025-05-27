# Accommodation API Specification

## Overview
The Accommodation API Service provides information about accommodation options in Swakopmund, Namibia. This RESTful API allows clients to retrieve accommodation listings, detailed information, and manage reviews.

## Base URL
```
http://localhost:8585
```

## Endpoints

### 1. Get Accommodations List
**Endpoint:** `GET /api/accommodations/`

**Description:** Retrieve a list of all available accommodations with optional name filtering.

**Query Parameters:**
- `name` (optional): Filter accommodations by name (case-insensitive partial match)

**Example Requests:**
```bash
GET /api/accommodations/
GET /api/accommodations/?name=hotel
```

**Response Format:**
```json
[
  {
    "id": 1,
    "name": "Swakopmund Hotel & Entertainment Centre",
    "description": "Located in the heart of Swakopmund...",
    "location": "2 Theo-Ben Gurirab Ave, Swakopmund",
    "website_url": "https://swakopmund-hotel.com",
    "mobile": "+264 64 410 200",
    "telephone": "+264 64 410 200",
    "email": "reservations@swakopmund-hotel.com",
    "images": [
      {
        "id": 1,
        "document_id": "img_1_1",
        "image_url": "https://example.com/images/accommodation_1_image_1.jpg",
        "accommodation_id": 1
      }
    ]
  }
]
```

### 2. Get Accommodation Details
**Endpoint:** `GET /api/accommodations/{id}`

**Description:** Retrieve detailed information about a specific accommodation including reviews.

**Path Parameters:**
- `id` (integer): The unique identifier of the accommodation

**Example Request:**
```bash
GET /api/accommodations/1
```

**Response Format:**
```json
{
  "id": 1,
  "name": "Swakopmund Hotel & Entertainment Centre",
  "description": "Located in the heart of Swakopmund...",
  "location": "2 Theo-Ben Gurirab Ave, Swakopmund",
  "website_url": "https://swakopmund-hotel.com",
  "mobile": "+264 64 410 200",
  "telephone": "+264 64 410 200",
  "email": "reservations@swakopmund-hotel.com",
  "images": [
    {
      "id": 1,
      "document_id": "img_1_1",
      "image_url": "https://example.com/images/accommodation_1_image_1.jpg",
      "accommodation_id": 1
    }
  ],
  "reviews": [
    {
      "id": 1,
      "user_id": 101,
      "rating": 4.5,
      "comment": "Great location and friendly staff!",
      "accommodation_id": 1
    }
  ]
}
```

**Error Responses:**
- `404 Not Found`: Accommodation with the specified ID does not exist
- `400 Bad Request`: Invalid accommodation ID format

### 3. Add Review
**Endpoint:** `POST /api/accommodations/{id}/reviews`

**Description:** Add a review for a specific accommodation.

**Path Parameters:**
- `id` (integer): The unique identifier of the accommodation

**Request Body:**
```json
{
  "user_id": 123,
  "rating": 4.5,
  "comment": "Great place to stay!"
}
```

**Required Fields:**
- `user_id` (integer): Unique identifier of the user submitting the review
- `rating` (float): Rating value between 0.0 and 5.0
- `comment` (string): Review comment/description

**Example Request:**
```bash
POST /api/accommodations/1/reviews
Content-Type: application/json

{
  "user_id": 456,
  "rating": 4.8,
  "comment": "Excellent service and beautiful location!"
}
```

**Success Response:**
```json
{
  "status": "success",
  "status_code": 200
}
```

**Error Responses:**
- `400 Bad Request`: Missing required fields or invalid data format
- `404 Not Found`: Accommodation with the specified ID does not exist

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200  | OK - Request successful |
| 400  | Bad Request - Invalid request format or missing required fields |
| 404  | Not Found - Resource not found |
| 500  | Internal Server Error - Server error occurred |

## CORS Support
All endpoints support Cross-Origin Resource Sharing (CORS) with the following headers:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type`

## Data Models

### Accommodation
```json
{
  "id": "integer",
  "name": "string",
  "description": "string",
  "location": "string",
  "website_url": "string",
  "mobile": "string",
  "telephone": "string",
  "email": "string"
}
```

### AccommodationImage
```json
{
  "id": "integer",
  "document_id": "string",
  "image_url": "string",
  "accommodation_id": "integer"
}
```

### Review
```json
{
  "id": "integer",
  "user_id": "integer",
  "rating": "float",
  "comment": "string",
  "accommodation_id": "integer"
}
```

## Example Usage

### Using curl

```bash
# Get all accommodations
curl -X GET "http://localhost:8585/api/accommodations/"

# Get accommodations filtered by name
curl -X GET "http://localhost:8585/api/accommodations/?name=hotel"

# Get specific accommodation details
curl -X GET "http://localhost:8585/api/accommodations/1"

# Add a review
curl -X POST "http://localhost:8585/api/accommodations/1/reviews" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 123, "rating": 4.5, "comment": "Great place!"}'
```

### Using JavaScript fetch

```javascript
// Get accommodations
const accommodations = await fetch('http://localhost:8585/api/accommodations/')
  .then(response => response.json());

// Add a review
const reviewResponse = await fetch('http://localhost:8585/api/accommodations/1/reviews', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user_id: 123,
    rating: 4.5,
    comment: 'Excellent accommodation!'
  })
});
``` 