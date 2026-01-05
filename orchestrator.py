from __future__ import annotations

import asyncio
import logging
from asyncio import Queue
from collections.abc import Awaitable
from contextlib import AbstractAsyncContextManager
from contextlib import contextmanager
from contextlib import suppress
from dataclasses import dataclass
from typing import NamedTuple

from base_runner import BaseScanResult
from zap_runner import zap_scan


class TaskId(NamedTuple):
    scanner: str
    url: str


class Result(NamedTuple):
    id: TaskId
    scan_result: BaseScanResult


@dataclass(frozen=True)
class _Task:
    id: TaskId
    func: Awaitable

    def __repr__(self) -> str:
        return f"<Task '{self.id.scanner} -> {self.id.url}'>" 


class Orchestrator(AbstractAsyncContextManager):

    _WORKERS_NUMBER = 2

    def __init__(self):
        self._tasks: Queue[_Task] = Queue()
        self._results: Queue[Result] = Queue()
        self._workers: list[_Worker] = []

    async def scan(self, scanner: str, url: str) -> TaskId:
        task_id = TaskId(scanner, url)
        match scanner:
            case 'zap': 
                task = _Task(task_id, zap_scan(url, scan_type='full'))
            case error_scanner:
                raise RuntimeError(f"Unexpected scanner value {error_scanner!r}")
        await self._tasks.put(task)
        _logger.debug("%r added", task)
        return task_id
    
    async def next_result(self) -> Result:
        while True:
            if self._results.empty() and self._tasks.empty() and not self._is_any_task_processing():
                raise NoMoreResults()
            with suppress(TimeoutError):
                return await asyncio.wait_for(self._results.get(), timeout=1)

    async def __aenter__(self) -> Orchestrator:
        for worker_no in range(1, self._WORKERS_NUMBER + 1):
            name = f"worker_{worker_no}"
            self._workers.append(_Worker(name, self._tasks, self._results))
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        for worker in self._workers:
            worker.send_stop_signal()
        for worker in self._workers:
            await worker.wait_until_stopped()
        self._workers = []

    def _is_any_task_processing(self) -> bool:
        return any([w.is_busy() for w in self._workers])


class NoMoreResults(Exception):
    pass


class _Worker:

    def __init__(self, name: str, tasks: Queue[_Task], results: Queue[Result]):
        self._name = name
        self._tasks = tasks
        self._results = results
        self._in_processing = False
        self._to_stop = False
        self._async_task = asyncio.get_running_loop().create_task(self._target())

    def send_stop_signal(self):
        self._to_stop = True

    def is_busy(self) -> bool:
        return self._in_processing
    
    async def wait_until_stopped(self):
        await asyncio.gather(self._async_task)

    async def _target(self):
        _logger.debug("Worker %s started", self._name)
        while True:
            try:
                task = await asyncio.wait_for(self._tasks.get(), timeout=1)
            except TimeoutError:
                if self._to_stop:
                    break
                continue
            with self._processing():
                scan_result = await task.func
            await self._results.put(Result(task.id, scan_result))
        _logger.debug("Worker %s stopped", self._name)

    @contextmanager
    def _processing(self):
        self._in_processing = True
        yield
        self._in_processing = False


_logger = logging.getLogger(__name__)
