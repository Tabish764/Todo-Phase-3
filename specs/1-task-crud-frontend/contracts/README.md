# API Contracts: Task CRUD Frontend

## Note on Backend API

This implementation is frontend-only with local state management as specified in the feature requirements. There are no backend API endpoints to define for this phase. The frontend will manage all task data in browser memory with optional localStorage persistence.

## Frontend Service Contracts

### TaskService Interface

```typescript
interface TaskService {
  getAllTasks(): Promise<Task[]>;
  createTask(taskData: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>): Promise<Task>;
  updateTask(id: string, taskData: Partial<Task>): Promise<Task>;
  deleteTask(id: string): Promise<boolean>;
  toggleTaskCompletion(id: string): Promise<Task>;
  saveToStorage(tasks: Task[]): void;
  loadFromStorage(): Task[] | null;
}
```

### Event Contracts

The frontend components will communicate through React props and state management rather than API calls:

- **TaskList** → **TaskItem**: Pass task data and action handlers
- **TaskForm** → **Parent**: Emit create/update events with task data
- **TaskItem** → **Parent**: Emit update/delete/toggle events with task ID

## Future API Contracts

When backend integration is added in a future phase, the following endpoints would be implemented:

```
POST   /api/tasks          - Create new task
GET    /api/tasks          - Get all tasks for user
GET    /api/tasks/{id}     - Get specific task
PUT    /api/tasks/{id}     - Update task
DELETE /api/tasks/{id}     - Delete task
PATCH  /api/tasks/{id}/toggle  - Toggle completion status
```

These contracts are documented for future reference when backend integration occurs.