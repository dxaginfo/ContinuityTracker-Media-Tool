# ContinuityTracker API Reference

This document provides details on the ContinuityTracker RESTful API for developers integrating with the platform.

## Authentication

All API requests require authentication using JWT tokens.

### Get Authentication Token

```
POST /api/auth/login
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

**Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user123",
    "email": "user@example.com",
    "name": "Demo User"
  }
}
```

### Using the Token

Include the token in the Authorization header for all API requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Refresh Token

```
POST /api/auth/refresh
```

**Request Headers:**

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Projects

### List Projects

```
GET /api/projects
```

**Response:**

```json
{
  "projects": [
    {
      "id": "project123",
      "name": "My Project",
      "description": "Project description",
      "created_at": "2025-06-22T15:30:45Z",
      "updated_at": "2025-06-22T15:30:45Z"
    }
  ]
}
```

### Create Project

```
POST /api/projects
```

**Request Body:**

```json
{
  "name": "New Project",
  "description": "Project description",
  "settings": {
    "default_continuity_rules": ["object_tracking", "clothing"]
  }
}
```

**Response:**

```json
{
  "project": {
    "id": "project456",
    "name": "New Project",
    "description": "Project description",
    "created_at": "2025-06-23T10:15:30Z",
    "updated_at": "2025-06-23T10:15:30Z",
    "settings": {
      "default_continuity_rules": ["object_tracking", "clothing"]
    }
  }
}
```

### Get Project

```
GET /api/projects/{id}
```

**Response:**

```json
{
  "project": {
    "id": "project456",
    "name": "New Project",
    "description": "Project description",
    "created_at": "2025-06-23T10:15:30Z",
    "updated_at": "2025-06-23T10:15:30Z",
    "settings": {
      "default_continuity_rules": ["object_tracking", "clothing"]
    }
  }
}
```

### Update Project

```
PUT /api/projects/{id}
```

**Request Body:**

```json
{
  "name": "Updated Project Name",
  "description": "Updated description",
  "settings": {
    "default_continuity_rules": ["object_tracking", "clothing", "lighting"]
  }
}
```

**Response:**

```json
{
  "project": {
    "id": "project456",
    "name": "Updated Project Name",
    "description": "Updated description",
    "created_at": "2025-06-23T10:15:30Z",
    "updated_at": "2025-06-23T11:20:15Z",
    "settings": {
      "default_continuity_rules": ["object_tracking", "clothing", "lighting"]
    }
  }
}
```

### Delete Project

```
DELETE /api/projects/{id}
```

**Response:**

```json
{
  "message": "Project deleted successfully"
}
```

## Assets

### Upload Asset

```
POST /api/projects/{id}/assets
```

**Request Body (multipart/form-data):**

- `file`: The media file (video or image)
- `metadata`: JSON string with asset metadata

```json
{
  "scene_info": {
    "scene_number": "5A",
    "shot_number": "3"
  },
  "timestamp": "2025-06-23T12:30:00Z",
  "tags": ["interior", "day"]
}
```

**Response:**

```json
{
  "asset": {
    "asset_id": "asset789",
    "project_id": "project456",
    "filename": "shot_5A_3.mp4",
    "url": "https://storage.googleapis.com/...",
    "content_type": "video/mp4",
    "type": "video",
    "uploaded_at": "2025-06-23T12:35:45Z",
    "metadata": {
      "scene_info": {
        "scene_number": "5A",
        "shot_number": "3"
      },
      "timestamp": "2025-06-23T12:30:00Z",
      "tags": ["interior", "day"]
    }
  }
}
```

### List Assets

```
GET /api/projects/{id}/assets
```

**Query Parameters:**

- `scene`: Filter by scene number
- `type`: Filter by asset type (video, image)
- `tags`: Filter by tags (comma-separated)

**Response:**

```json
{
  "assets": [
    {
      "asset_id": "asset789",
      "project_id": "project456",
      "filename": "shot_5A_3.mp4",
      "url": "https://storage.googleapis.com/...",
      "content_type": "video/mp4",
      "type": "video",
      "uploaded_at": "2025-06-23T12:35:45Z",
      "metadata": {
        "scene_info": {
          "scene_number": "5A",
          "shot_number": "3"
        },
        "timestamp": "2025-06-23T12:30:00Z",
        "tags": ["interior", "day"]
      }
    }
  ]
}
```

### Get Asset

```
GET /api/projects/{id}/assets/{asset_id}
```

**Response:**

```json
{
  "asset": {
    "asset_id": "asset789",
    "project_id": "project456",
    "filename": "shot_5A_3.mp4",
    "url": "https://storage.googleapis.com/...",
    "content_type": "video/mp4",
    "type": "video",
    "uploaded_at": "2025-06-23T12:35:45Z",
    "metadata": {
      "scene_info": {
        "scene_number": "5A",
        "shot_number": "3"
      },
      "timestamp": "2025-06-23T12:30:00Z",
      "tags": ["interior", "day"]
    }
  }
}
```

### Delete Asset

```
DELETE /api/projects/{id}/assets/{asset_id}
```

**Response:**

```json
{
  "message": "Asset deleted successfully"
}
```

## Analysis

### Run Analysis

```
POST /api/projects/{id}/analyze
```

**Request Body:**

```json
{
  "continuity_rules": [
    {
      "rule_type": "object_tracking",
      "priority": "high",
      "description": "Track key props"
    },
    {
      "rule_type": "clothing",
      "priority": "medium",
      "description": "Check costume consistency"
    }
  ],
  "media_assets": ["asset789", "asset790", "asset791"],
  "notification_settings": {
    "email": "user@example.com",
    "slack_webhook": "https://hooks.slack.com/...",
    "severity_threshold": "warning"
  }
}
```

**Response:**

```json
{
  "analysis_id": "analysis123",
  "status": "processing"
}
```

### Get Analysis Status

```
GET /api/projects/{id}/analysis/{analysis_id}
```

**Response:**

```json
{
  "analysis": {
    "id": "analysis123",
    "project_id": "project456",
    "status": "completed",
    "created_at": "2025-06-23T14:10:30Z",
    "completed_at": "2025-06-23T14:15:45Z",
    "results": {
      "project_id": "project456",
      "analysis_id": "analysis123",
      "timestamp": "2025-06-23T14:15:45Z",
      "continuity_issues": [
        {
          "issue_id": "issue001",
          "type": "object_mismatch",
          "severity": "warning",
          "description": "Coffee mug changes color between scenes",
          "affected_assets": ["asset789", "asset791"],
          "affected_scenes": ["5A", "5C"],
          "frames": [123, 45],
          "confidence_score": 0.92,
          "suggested_resolution": "Ensure consistent mug color"
        }
      ],
      "summary": {
        "total_issues": 1,
        "by_severity": {
          "error": 0,
          "warning": 1,
          "info": 0
        },
        "by_type": {
          "object_mismatch": 1
        }
      }
    }
  }
}
```

### List Analyses

```
GET /api/projects/{id}/analysis
```

**Response:**

```json
{
  "analyses": [
    {
      "id": "analysis123",
      "project_id": "project456",
      "status": "completed",
      "created_at": "2025-06-23T14:10:30Z",
      "completed_at": "2025-06-23T14:15:45Z"
    },
    {
      "id": "analysis124",
      "project_id": "project456",
      "status": "pending",
      "created_at": "2025-06-23T15:20:10Z",
      "completed_at": null
    }
  ]
}
```

## Continuity Rules

### List Rules

```
GET /api/rules
```

**Response:**

```json
{
  "rules": [
    {
      "id": "rule001",
      "rule_type": "object_tracking",
      "name": "Prop Tracking",
      "description": "Track key props across scenes",
      "priority": "high",
      "created_at": "2025-06-20T10:15:30Z",
      "created_by": "user123",
      "is_global": true,
      "parameters": {
        "min_confidence": 0.8
      }
    }
  ]
}
```

### Create Rule

```
POST /api/rules
```

**Request Body:**

```json
{
  "rule_type": "lighting",
  "name": "Lighting Consistency",
  "description": "Check for lighting direction and color consistency",
  "priority": "medium",
  "is_global": false,
  "project_id": "project456",
  "parameters": {
    "sensitivity": "high",
    "check_color_temperature": true
  }
}
```

**Response:**

```json
{
  "rule": {
    "id": "rule002",
    "rule_type": "lighting",
    "name": "Lighting Consistency",
    "description": "Check for lighting direction and color consistency",
    "priority": "medium",
    "created_at": "2025-06-23T16:30:45Z",
    "created_by": "user123",
    "is_global": false,
    "project_id": "project456",
    "parameters": {
      "sensitivity": "high",
      "check_color_temperature": true
    }
  }
}
```

### Get Rule

```
GET /api/rules/{id}
```

**Response:**

```json
{
  "rule": {
    "id": "rule002",
    "rule_type": "lighting",
    "name": "Lighting Consistency",
    "description": "Check for lighting direction and color consistency",
    "priority": "medium",
    "created_at": "2025-06-23T16:30:45Z",
    "created_by": "user123",
    "is_global": false,
    "project_id": "project456",
    "parameters": {
      "sensitivity": "high",
      "check_color_temperature": true
    }
  }
}
```

### Update Rule

```
PUT /api/rules/{id}
```

**Request Body:**

```json
{
  "name": "Updated Lighting Rule",
  "description": "Updated description",
  "priority": "high",
  "parameters": {
    "sensitivity": "medium",
    "check_color_temperature": true,
    "check_shadows": true
  }
}
```

**Response:**

```json
{
  "rule": {
    "id": "rule002",
    "rule_type": "lighting",
    "name": "Updated Lighting Rule",
    "description": "Updated description",
    "priority": "high",
    "created_at": "2025-06-23T16:30:45Z",
    "updated_at": "2025-06-23T17:45:10Z",
    "created_by": "user123",
    "is_global": false,
    "project_id": "project456",
    "parameters": {
      "sensitivity": "medium",
      "check_color_temperature": true,
      "check_shadows": true
    }
  }
}
```

### Delete Rule

```
DELETE /api/rules/{id}
```

**Response:**

```json
{
  "message": "Rule deleted successfully"
}
```

## Webhooks

ContinuityTracker supports webhooks for event-driven integrations.

### Register Webhook

```
POST /api/webhooks
```

**Request Body:**

```json
{
  "url": "https://your-app.example.com/webhook",
  "events": ["analysis.completed", "issue.created"],
  "project_id": "project456",
  "secret": "your-webhook-secret"
}
```

**Response:**

```json
{
  "webhook": {
    "id": "webhook001",
    "url": "https://your-app.example.com/webhook",
    "events": ["analysis.completed", "issue.created"],
    "project_id": "project456",
    "created_at": "2025-06-23T18:10:30Z"
  }
}
```

### Webhook Payload Examples

**Analysis Completed Event:**

```json
{
  "event": "analysis.completed",
  "timestamp": "2025-06-23T19:15:45Z",
  "data": {
    "analysis_id": "analysis123",
    "project_id": "project456",
    "status": "completed",
    "issue_count": 3,
    "url": "https://continuity-tracker-app.example.com/projects/project456/analysis/analysis123"
  }
}
```

**Issue Created Event:**

```json
{
  "event": "issue.created",
  "timestamp": "2025-06-23T19:16:30Z",
  "data": {
    "issue_id": "issue001",
    "analysis_id": "analysis123",
    "project_id": "project456",
    "type": "object_mismatch",
    "severity": "warning",
    "url": "https://continuity-tracker-app.example.com/projects/project456/analysis/analysis123/issues/issue001"
  }
}
```

## Error Responses

Error responses follow a standard format:

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {} // Optional additional details
}
```

### Common Error Codes

- `AUTHENTICATION_REQUIRED`: Missing or invalid authentication token
- `INVALID_CREDENTIALS`: Incorrect email or password
- `FORBIDDEN`: User does not have permission for the requested resource
- `NOT_FOUND`: Requested resource not found
- `VALIDATION_ERROR`: Invalid request parameters
- `INTERNAL_ERROR`: Server error

## Rate Limiting

API requests are subject to rate limiting. The current limits are:

- 100 requests per minute per user
- 5 concurrent analysis jobs per project

Rate limit information is included in response headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1624460400
```

When rate limited, the API returns a 429 Too Many Requests status code.