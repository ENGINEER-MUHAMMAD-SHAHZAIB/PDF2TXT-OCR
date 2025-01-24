# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0
"""Semaphore-free alternate executor.

There are two popular environments that do not fully support the standard Python
multiprocessing module: AWS Lambda, and Termux (a terminal emulator for Android).

This alternate executor divvies up work among worker processes before processing,
rather than having each worker consume work from a shared queue when they finish
their task. This means workers have no need to coordinate with each other. Each
worker communicates only with the main process.

This is not without drawbacks. If the tasks are not "even" in size, which cannot
be guaranteed, some workers may end up with too much work while others are idle.
It is less efficient than the standard implementation, so not the default.
"""

from __future__ import annotations

import logging
import logging.handlers
import signal
from collections.abc import Callable, Iterable, Iterator
from contextlib import suppress
from enum import Enum, auto
from itertools import islice, repeat, takewhile, zip_longest
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection, wait

from ocrmypdf import Executor, hookimpl
from ocrmypdf._concurrent import NullProgressBar
from ocrmypdf.exceptions import InputFileError
from ocrmypdf.helpers import remove_all_log_handlers


class MessageType(Enum):
    """Implement basic IPC messaging."""

    exception = auto()  # pylint: disable=invalid-name
    result = auto()  # pylint: disable=invalid-name
    complete = auto()  # pylint: disable=invalid-name


def split_every(n: int, iterable: Iterable) -> Iterator:
    """Split iterable into groups of n.

    >>> list(split_every(4, range(10)))
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    https://stackoverflow.com/a/22919323
    """
    iterator = iter(iterable)
    return takewhile(bool, (list(islice(iterator, n)) for _ in repeat(None)))


def process_sigbus(*args):
    """Handle SIGBUS signal at the worker level."""
    raise InputFileError("A worker process lost access to an input file")


class ConnectionLogHandler(logging.handlers.QueueHandler):
    """Handler used by child processes to forward log messages to parent."""

    def __init__(self, conn: Connection) -> None:
        """Initialize the handler."""
        # sets the parent's queue to None - parent only touches queue
        # in enqueue() which we override
        super().__init__(None)  # type: ignore
        self.conn = conn

    def enqueue(self, record):
        """Enqueue a log message."""
        self.conn.send(('log', record))


def process_loop(
    conn: Connection, user_init: Callable[[], None], loglevel, task, task_args
):
    """Initialize a process pool worker."""
    # Install SIGBUS handler (so our parent process can abort somewhat gracefully)
    with suppress(AttributeError):  # Windows and Cygwin do not have SIGBUS
        # Windows and Cygwin do not have pthread_sigmask or SIGBUS
        signal.signal(signal.SIGBUS, process_sigbus)

    # Reconfigure the root logger for this process to send all messages to a queue
    h = ConnectionLogHandler(conn)
    root = logging.getLogger()
    remove_all_log_handlers(root)
    root.setLevel(loglevel)
    root.addHandler(h)

    user_init()

    for args in task_args:
        try:
            result = task(*args)
        except Exception as e:  # pylint: disable=broad-except
            conn.send((MessageType.exception, e))
            break
        else:
            conn.send((MessageType.result, result))

    conn.send((MessageType.complete, None))
    conn.close()
    return


class LambdaExecutor(Executor):
    """Executor for AWS Lambda or similar environments that lack semaphores."""

    def _execute(
        self,
        *,
        use_threads: bool,
        max_workers: int,
        progress_kwargs: dict,
        worker_initializer: Callable,
        task: Callable,
        task_arguments: Iterable,
        task_finished: Callable,
    ):
        if use_threads and max_workers == 1:
            with self.pbar_class(**progress_kwargs) as pbar:
                for args in task_arguments:
                    result = task(*args)
                    task_finished(result, pbar)
            return

        task_arguments = list(task_arguments)
        grouped_args = list(
            zip_longest(*list(split_every(max_workers, task_arguments)))
        )
        if not grouped_args:
            return

        processes: list[Process] = []
        connections: list[Connection] = []
        for chunk in grouped_args:
            parent_conn, child_conn = Pipe()

            worker_args = [args for args in chunk if args is not None]
            process = Process(
                target=process_loop,
                args=(
                    child_conn,
                    worker_initializer,
                    logging.getLogger("").level,
                    task,
                    worker_args,
                ),
            )
            process.daemon = True
            processes.append(process)
            connections.append(parent_conn)

        for process in processes:
            process.start()

        with self.pbar_class(**progress_kwargs) as pbar:
            while connections:
                for result in wait(connections):
                    if not isinstance(result, Connection):
                        raise NotImplementedError("We only support Connection()")
                    try:
                        msg_type, msg = result.recv()
                    except EOFError:
                        connections.remove(result)
                        continue

                    if msg_type == MessageType.result:
                        task_finished(msg, pbar)
                    elif msg_type == 'log':
                        record = msg
                        logger = logging.getLogger(record.name)
                        logger.handle(record)
                    elif msg_type == MessageType.complete:
                        connections.remove(result)
                    elif msg_type == MessageType.exception:
                        for process in processes:
                            process.terminate()
                        raise msg

        for process in processes:
            process.join()


@hookimpl
def get_executor(progressbar_class):
    """Return a LambdaExecutor instance."""
    return LambdaExecutor(pbar_class=progressbar_class)


@hookimpl
def get_logging_console():
    """Return a logging.StreamHandler instance."""
    return logging.StreamHandler()


@hookimpl
def get_progressbar_class():
    """Return a NullProgressBar instance.

    This executor cannot use a progress bar.
    """
    return NullProgressBar
