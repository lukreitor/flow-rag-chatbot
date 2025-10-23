from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Callable, Optional

from redis import Redis
from rq import Queue

from app.core.config import get_settings


@dataclass
class TaskResult:
    status: str
    payload: Any
    job_id: str


class TaskQueue:
    """Thin wrapper around RQ queue for Flow API tasks."""

    def __init__(self, redis_url: Optional[str] = None, queue_name: Optional[str] = None):
        settings = get_settings()
        self._connection = Redis.from_url(redis_url or settings.redis_url)
        self._queue = Queue(queue_name or settings.task_queue_name, connection=self._connection)

    def enqueue(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> TaskResult:
        job = self._queue.enqueue(func, *args, **kwargs)
        return TaskResult(status=job.get_status(), payload=None, job_id=job.id)

    def fetch(self, job_id: str) -> TaskResult:
        job = self._queue.fetch_job(job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")
        job.refresh()
        return TaskResult(status=job.get_status(), payload=job.result, job_id=job.id)

    def wait_for_result(self, job_id: str, timeout: int = 30, poll_interval: float = 0.5) -> TaskResult:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            job = self._queue.fetch_job(job_id)
            if not job:
                raise ValueError(f"Job {job_id} not found")
            job.refresh()
            if job.is_finished:
                return TaskResult(status=job.get_status(), payload=job.result, job_id=job.id)
            if job.is_failed:
                raise RuntimeError(f"Job {job_id} failed: {job.exc_info}")
            time.sleep(poll_interval)

        raise TimeoutError(f"Job {job_id} did not finish within {timeout} seconds")
