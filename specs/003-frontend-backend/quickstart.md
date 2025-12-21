# Quickstart: Frontend-Backend Integration

## Overview
This guide explains how to connect the frontend Todo application to the backend API.

## Prerequisites
- Backend API running on `http://localhost:8000`
- Frontend application set up and running

## API Configuration
The frontend needs to be configured with the backend API URL:

```javascript
// API configuration
const API_BASE_URL = 'http://localhost:8000';
const TASKS_ENDPOINT = `${API_BASE_URL}/tasks`;
```

## API Endpoints

### GET /tasks
Retrieve all tasks
```javascript
// Example request
fetch('http://localhost:8000/tasks')
  .then(response => response.json())
  .then(tasks => console.log(tasks));
```

### POST /tasks
Create a new task
```javascript
// Example request
fetch('http://localhost:8000/tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'New task',
    description: 'Task description'
  })
})
```

### PUT /tasks/{id}
Update a task
```javascript
// Example request
fetch('http://localhost:8000/tasks/task-id-123', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    completed: true
  })
})
```

### DELETE /tasks/{id}
Delete a task
```javascript
// Example request
fetch('http://localhost:8000/tasks/task-id-123', {
  method: 'DELETE'
})
```

## Error Handling
The API returns the following status codes:
- `200`: Success for GET, PUT
- `201`: Success for POST (created)
- `204`: Success for DELETE (no content)
- `404`: Resource not found
- `422`: Validation error

## Validation Rules
- Task title must be 1-200 characters
- Task description is optional
- Task completion status is a boolean