# Swakopmund Backend Services

The backend services use a microservices architecture where services exist independently of other services and are connected via a gateway.

## Services

### Authentication Service

The authentication service is responsible for handling user authentication and authorization.

### Property Management Service

The property management service is responsible for managing properties.

### Restaurant Service

The restaurant service is responsible for managing restaurants.

### Waste Management Service

The waste management service is responsible for managing waste.

### Activities Service

The activities service is responsible for managing activities.

### Place of Interest Service

The place of interest service is responsible for managing points of interest.

### Events Service

The events service is responsible for managing events.

### Notifications Service

The notifications service is responsible for sending notifications.

## Communication

In order to communicate with the services, the gateway redirects all requests to the appropriate service, via an Nginx reverse proxy.

## Deployment

The services are each containerised with their own database and are orchestrated via Docker Compose.

To run the backend, ensure you're in the root directory and run the command:
```bash
docker compose up -d --build
```

Anytime changes are made to the services, the containers need to be rebuild with the same command.