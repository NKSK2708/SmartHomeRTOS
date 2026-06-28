"""Minimal RTOS-like simulation utilities (queues, task helper).
This is intentionally small and dependency-free for portability.
"""
import threading
import queue
import time
from typing import Any, Dict

class EventQueue:
    def __init__(self):
        self._q = queue.Queue()

    def put(self, item: Dict[str, Any]):
        self._q.put(item)

    def get(self, timeout=None):
        try:
            return self._q.get(timeout=timeout)
        except queue.Empty:
            raise

class TaskThread(threading.Thread):
    def __init__(self, name: str, target, args=()):
        super().__init__(name=name, daemon=True)
        self._target = target
        self._args = args

    def run(self):
        try:
            self._target(*self._args)
        except Exception as e:
            print(f"[TaskThread:{self.name}] crashed: {e}")

"""End of rtos utilities"""