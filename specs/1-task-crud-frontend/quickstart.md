# Quickstart Guide: Task CRUD Frontend

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Setup Instructions

### 1. Clone or Initialize the Project

```bash
# If this is a new project, initialize Next.js app
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"

# Or if the project already exists, navigate to the frontend directory
cd frontend
```

### 2. Install Dependencies

```bash
cd frontend
npm install
```

### 3. Project Structure

After setup, your project should have this structure:

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── TaskList/
│   │   │   └── TaskList.tsx
│   │   ├── TaskItem/
│   │   │   └── TaskItem.tsx
│   │   └── TaskForm/
│   │       └── TaskForm.tsx
│   ├── hooks/
│   │   └── useTaskManager.ts
│   ├── types/
│   │   └── task.ts
│   └── utils/
│       └── storage.ts
├── public/
├── package.json
└── tailwind.config.ts
```

### 4. Key Component Implementation

#### Task Type Definition (`src/types/task.ts`)

```typescript
export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
}
```

#### Storage Utility (`src/utils/storage.ts`)

```typescript
const STORAGE_KEY = 'task-manager-data';

export const loadTasksFromStorage = (): Task[] | null => {
  if (typeof window === 'undefined') return null;

  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return null;

    const parsed = JSON.parse(stored);
    // Convert string dates back to Date objects
    return parsed.tasks?.map((task: any) => ({
      ...task,
      createdAt: new Date(task.createdAt),
      updatedAt: new Date(task.updatedAt)
    })) || null;
  } catch (error) {
    console.error('Error loading tasks from storage:', error);
    return null;
  }
};

export const saveTasksToStorage = (tasks: Task[]): void => {
  if (typeof window === 'undefined') return;

  try {
    const dataToStore = {
      tasks,
      lastUpdated: new Date().toISOString()
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(dataToStore));
  } catch (error) {
    console.error('Error saving tasks to storage:', error);
  }
};
```

#### Task Manager Hook (`src/hooks/useTaskManager.ts`)

```typescript
import { useState, useEffect } from 'react';
import { Task } from '@/types/task';
import { loadTasksFromStorage, saveTasksToStorage } from '@/utils/storage';

export const useTaskManager = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  // Load tasks from storage on mount
  useEffect(() => {
    const storedTasks = loadTasksFromStorage();
    if (storedTasks) {
      setTasks(storedTasks);
    }
    setLoading(false);
  }, []);

  // Save tasks to storage whenever tasks change
  useEffect(() => {
    if (!loading) {
      saveTasksToStorage(tasks);
    }
  }, [tasks, loading]);

  const createTask = (title: string, description?: string): Task => {
    const newTask: Task = {
      id: `task_${Date.now()}`, // Simple ID generation
      title,
      description,
      completed: false,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    setTasks(prev => [...prev, newTask]);
    return newTask;
  };

  const updateTask = (id: string, updates: Partial<Task>): Task | null => {
    setTasks(prev =>
      prev.map(task => {
        if (task.id === id) {
          const updatedTask = {
            ...task,
            ...updates,
            updatedAt: new Date()
          };
          return updatedTask;
        }
        return task;
      })
    );

    const updatedTask = tasks.find(task => task.id === id);
    return updatedTask ? {
      ...updatedTask,
      ...updates,
      updatedAt: new Date()
    } : null;
  };

  const deleteTask = (id: string): boolean => {
    const taskExists = tasks.some(task => task.id === id);
    if (taskExists) {
      setTasks(prev => prev.filter(task => task.id !== id));
      return true;
    }
    return false;
  };

  const toggleTaskCompletion = (id: string): Task | null => {
    const task = tasks.find(t => t.id === id);
    if (task) {
      return updateTask(id, { completed: !task.completed });
    }
    return null;
  };

  return {
    tasks,
    loading,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion
  };
};
```

### 5. Running the Application

```bash
# Development mode
npm run dev

# The app will be available at http://localhost:3000
```

### 6. Testing

```bash
# Run unit tests
npm test

# Run component tests
npm run test:components
```

### 7. Build for Production

```bash
# Build the application
npm run build

# Start production server
npm start
```

## Component Usage

### TaskList Component

The main component that displays all tasks and provides the interface for managing them.

### TaskForm Component

Handles creating new tasks and editing existing ones.

### TaskItem Component

Displays individual tasks with controls for completion, editing, and deletion.

## Environment Configuration

No special environment variables are required for this frontend-only implementation. All data is stored locally in the browser.

For future backend integration, you would add:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Troubleshooting

- **Tasks not persisting**: Ensure localStorage is enabled in the browser
- **TypeScript errors**: Run `npm install --save-dev typescript @types/node @types/react @types/react-dom`
- **Tailwind not working**: Verify tailwind.config.ts and globals.css are properly configured