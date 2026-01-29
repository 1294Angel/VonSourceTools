"""
Threading utilities for long-running operations.

This module provides utilities to run operations in background threads
while keeping Blender responsive. Uses modal operators with timers
to check for completion.
"""
import threading
import queue
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, List, Dict
from enum import Enum


class TaskStatus(Enum):
    """Status of a background task."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskResult:
    """Result of a background task."""
    status: TaskStatus
    result: Any = None
    error: Optional[str] = None
    progress: float = 0.0
    message: str = ""


@dataclass
class BackgroundTask:
    """A task to be executed in a background thread."""
    func: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    _result: TaskResult = field(default_factory=lambda: TaskResult(TaskStatus.PENDING))
    _thread: Optional[threading.Thread] = None
    _cancelled: bool = False
    
    def start(self):
        """Start the task in a background thread."""
        self._result = TaskResult(TaskStatus.RUNNING, message="Starting...")
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
    
    def _run(self):
        """Execute the task function."""
        try:
            if self._cancelled:
                self._result = TaskResult(TaskStatus.CANCELLED, message="Task cancelled")
                return
            
            result = self.func(*self.args, **self.kwargs)
            
            if self._cancelled:
                self._result = TaskResult(TaskStatus.CANCELLED, message="Task cancelled")
                return
            
            self._result = TaskResult(
                TaskStatus.COMPLETED,
                result=result,
                progress=1.0,
                message="Completed successfully"
            )
        except Exception as e:
            self._result = TaskResult(
                TaskStatus.FAILED,
                error=str(e),
                message=f"Failed: {str(e)}"
            )
    
    def cancel(self):
        """Request cancellation of the task."""
        self._cancelled = True
    
    @property
    def is_running(self) -> bool:
        """Check if the task is still running."""
        return self._thread is not None and self._thread.is_alive()
    
    @property
    def is_finished(self) -> bool:
        """Check if the task has finished (success, failure, or cancelled)."""
        return self._result.status in (
            TaskStatus.COMPLETED, 
            TaskStatus.FAILED, 
            TaskStatus.CANCELLED
        )
    
    @property
    def result(self) -> TaskResult:
        """Get the current result/status of the task."""
        return self._result


class TaskManager:
    """
    Manages background tasks.
    
    Singleton instance to track all running tasks across the addon.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tasks = {}
            cls._instance._task_counter = 0
        return cls._instance
    
    def create_task(self, func: Callable, *args, **kwargs) -> str:
        """
        Create and start a new background task.
        
        Args:
            func: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Task ID string
        """
        self._task_counter += 1
        task_id = f"task_{self._task_counter}"
        
        task = BackgroundTask(func=func, args=args, kwargs=kwargs)
        self._tasks[task_id] = task
        task.start()
        
        return task_id
    
    def get_task(self, task_id: str) -> Optional[BackgroundTask]:
        """Get a task by ID."""
        return self._tasks.get(task_id)
    
    def remove_task(self, task_id: str):
        """Remove a completed task from tracking."""
        if task_id in self._tasks:
            del self._tasks[task_id]
    
    def cancel_task(self, task_id: str):
        """Cancel a running task."""
        task = self._tasks.get(task_id)
        if task:
            task.cancel()
    
    def get_all_running(self) -> List[str]:
        """Get IDs of all running tasks."""
        return [
            task_id for task_id, task in self._tasks.items()
            if task.is_running
        ]


# Global task manager instance
task_manager = TaskManager()


def run_in_background(func: Callable, *args, **kwargs) -> str:
    """
    Convenience function to run a function in the background.
    
    Args:
        func: Function to execute
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        Task ID for tracking
    """
    return task_manager.create_task(func, *args, **kwargs)


def get_task_result(task_id: str) -> Optional[TaskResult]:
    """
    Get the result of a background task.
    
    Args:
        task_id: Task ID returned from run_in_background
        
    Returns:
        TaskResult or None if task not found
    """
    task = task_manager.get_task(task_id)
    if task:
        return task.result
    return None


def is_task_finished(task_id: str) -> bool:
    """Check if a task has finished."""
    task = task_manager.get_task(task_id)
    if task:
        return task.is_finished
    return True  # Non-existent task is considered finished


def cleanup_task(task_id: str):
    """Remove a finished task from tracking."""
    task_manager.remove_task(task_id)
