export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
  pending?: boolean;     // Indicates operation in progress (create, update, delete)
  tempId?: string;       // Temporary UUID before server assigns real ID (for new tasks)
}