from typing import Dict, List, Optional
from src.database.models import Task


class InMemoryTaskDB:
    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def get_all_tasks(self) -> List[Task]:
        return list(self._tasks.values())

    def get_task(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)

    def create_task(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    def update_task(self, task_id: str, task: Task) -> Optional[Task]:
        if task_id in self._tasks:
            self._tasks[task_id] = task
            return task
        return None

    def delete_task(self, task_id: str) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False


# Global instance
db = InMemoryTaskDB()