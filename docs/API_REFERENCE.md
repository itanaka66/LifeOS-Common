# API Reference for LifeOS Platform

## Overview

This document provides the complete API reference for the LifeOS platform, including all endpoints, request/response formats, and authentication methods.

## Base URL

`https://api.lifeos.dev/v1`

## Authentication

All endpoints require authentication via Bearer Token:

```http
Authorization: Bearer <access_token>
```

### Token Generation

To obtain an access token, make a POST request to the login endpoint:

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Core Endpoints

### User Management

#### Get Current User Profile
```http
GET /users/me
Authorization: Bearer <access_token>
```

Response:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Update User Profile
```http
PUT /users/me
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "email": "newemail@example.com"
}
```

Response:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "newemail@example.com",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Delete User Account
```http
DELETE /users/me
Authorization: Bearer <access_token>
```

### Person Management

#### List All Persons
```http
GET /persons
Authorization: Bearer <access_token>
```

Response:
```json
{
  "persons": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "John Doe",
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

#### Create New Person
```http
POST /persons
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Jane Smith"
}
```

Response:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174001",
  "name": "Jane Smith",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Get Person by ID
```http
GET /persons/{id}
Authorization: Bearer <access_token>
```

Response:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Update Person
```http
PUT /persons/{id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "John Doe Updated"
}
```

Response:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe Updated",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Delete Person
```http
DELETE /persons/{id}
Authorization: Bearer <access_token>
```

### Document Management

#### List Documents
```http
GET /documents
Authorization: Bearer <access_token>
```

Response:
```json
{
  "documents": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "My Document",
      "file_id": "123e4567-e89b-12d3-a456-426614174001",
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

#### Upload Document
```http
POST /documents
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

{
  "file": "<file_content>",
  "title": "My Document"
}
```

Response:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "My Document",
  "file_id": "123e4567-e89b-12d3-a456-426614174001",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Get Document by ID
```http
GET /documents/{id}
Authorization: Bearer <access_token>
```

Response:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "My Document",
  "file_id": "123e4567-e89b-12d3-a456-426614174001",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Delete Document
```http
DELETE /documents/{id}
Authorization: Bearer <access_token>
```

## Plugin Endpoints

### Plugin Installation

#### Install Plugin
```http
POST /plugins/install
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "plugin_id": "lifeos.finance",
  "version": "2.1.0"
}
```

Response:
```json
{
  "status": "success",
  "message": "Plugin installed successfully",
  "plugin_id": "lifeos.finance",
  "version": "2.1.0"
}
```

### Migration Management

#### Run Plugin Migration
```http
POST /plugins/{plugin_id}/migrate
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "direction": "up"
}
```

Response:
```json
{
  "status": "success",
  "message": "Migration completed successfully",
  "plugin_id": "lifeos.finance",
  "migration_id": "0001_initial"
}
```

### Plugin Status

#### Get Plugin Status
```http
GET /plugins/status
Authorization: Bearer <access_token>
```

Response:
```json
{
  "plugins": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "plugin_id": "lifeos.finance",
      "version": "2.1.0",
      "status": "active",
      "enabled": true,
      "installed_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

## Event Bus Endpoints

### Subscribe to Events

#### Register Event Subscription
```http
POST /events/subscribe
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "event_type": "document.created",
  "callback_url": "https://yourapp.com/webhook"
}
```

Response:
```json
{
  "status": "success",
  "message": "Event subscription registered",
  "subscription_id": "123e4567-e89b-12d3-a456-426614174002"
}
```

#### List Event Subscriptions
```http
GET /events/subscriptions
Authorization: Bearer <access_token>
```

Response:
```json
{
  "subscriptions": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174002",
      "event_type": "document.created",
      "callback_url": "https://yourapp.com/webhook",
      "created_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

## Error Handling

### Standard Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description",
    "details": {
      "field": "field_name",
      "reason": "validation_error"
    }
  }
}
```

### Common HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Unprocessable Entity |
| 500 | Internal Server Error |

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Default**: 100 requests per minute
- **Premium users**: 1000 requests per minute
- **Admin users**: Unlimited requests

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1634567890
```

## Versioning

API versioning is handled through the URL path:
`https://api.lifeos.dev/v1/...`

All endpoints are versioned to ensure backward compatibility and allow for breaking changes when necessary.

## Pagination

For endpoints that return lists, pagination is supported:

```http
GET /persons?page=1&limit=20
Authorization: Bearer <access_token>
```

Response:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```