from queue import Queue
from abc import ABC, abstractmethod
from typing import Generator, Any, Optional


class SystemCall(ABC):
    """SystemCall yielded by Task to handle with Scheduler"""

    @abstractmethod
    def handle(self, scheduler: 'Scheduler', task: 'Task') -> bool:
        """
        :param scheduler: link to scheduler to manipulate with active tasks
        :param task: task which requested the system call
        :return: an indication that the task must be scheduled again
        """


Coroutine = Generator[SystemCall | None, Any, None]


class Task:
    def __init__(self, task_id: int, target: Coroutine) -> None:
        """
        :param task_id: id of the task
        :param target: coroutine to run. Coroutine can produce system calls.
        System calls are being executed by scheduler and the result sends back to coroutine.
        """
        self.task_id = task_id
        self.target = target
        self.is_running = True
        self.syscall_result: Optional[Any] = None

    def set_syscall_result(self, result: Any) -> None:
        """
        Saves result of the last system call
        """
        self.syscall_result = result

    def step(self) -> SystemCall | None:
        """
        Performs one step of coroutine, i.e. sends result of last system call
        to coroutine (generator), gets yielded value and returns it.
        """
        if not self.is_running:
            return None

        try:
            if self.syscall_result is not None:
                result = self.target.send(self.syscall_result)
                self.syscall_result = None
            else:
                result = next(self.target)

            if isinstance(result, SystemCall):
                return result

        except StopIteration:
            self.is_running = False

        return None


class Scheduler:
    """Scheduler to manipulate with tasks"""

    def __init__(self) -> None:
        self.task_id = 0
        self.task_queue: Queue[Task] = Queue()
        self.task_map: dict[int, Task] = {}  # task_id -> task
        self.wait_map: dict[int, list[Task]] = {}  # task_id -> list of waiting tasks

    def _schedule_task(self, task: Task) -> None:
        """
        Add task into task queue
        :param task: task to schedule for execution
        """
        self.task_queue.put(task)

    def new(self, target: Coroutine) -> int:
        """
        Create and schedule new task
        :param target: coroutine to wrap in task
        :return: id of newly created task
        """
        self.task_id += 1
        task = Task(self.task_id, target)
        self.task_map[self.task_id] = task
        self._schedule_task(task)
        return self.task_id

    def exit_task(self, task_id: int) -> bool:
        """
        PRIVATE API: can be used only from scheduler itself or system calls
        Hint: do not forget to reschedule waiting tasks
        :param task_id: task to remove from scheduler
        :return: true if task id is valid
        """
        if task_id in self.task_map:
            del self.task_map[task_id]

            if task_id in self.wait_map:
                for waiting_task in self.wait_map.pop(task_id, []):
                    self._schedule_task(waiting_task)

            self.wait_map.pop(task_id, None)
            return True

        return False

    def wait_task(self, task_id: int, wait_id: int) -> bool:
        """
        PRIVATE API: can be used only from scheduler itself or system calls
        :param task_id: task to hold on until another task is finished
        :param wait_id: id of the other task to wait for
        :return: true if task and wait ids are valid task ids
        """
        if wait_id in self.task_map and task_id in self.task_map:
            self.wait_map.setdefault(wait_id, []).append(self.task_map[task_id])
            return True

        return False

    def run(self, ticks: int | None = None) -> None:
        """
        Executes tasks consequently, gets yielded system calls,
        handles them and reschedules task if needed
        :param ticks: number of iterations (task steps), infinite if not passed
        """
        iterations = 0
        while not self.empty():
            if ticks is not None and iterations >= ticks:
                break

            task = self.task_queue.get()
            syscall = task.step()

            if isinstance(syscall, SystemCall):
                continue_execution = syscall.handle(self, task)
                if not continue_execution:
                    continue

            if task.is_running:
                self._schedule_task(task)
            else:
                self.exit_task(task.task_id)

            iterations += 1

    def empty(self) -> bool:
        """Checks if there are some scheduled tasks"""
        return not bool(self.task_map)


class GetTid(SystemCall):
    """System call to get current task id"""

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        task.set_syscall_result(task.task_id)
        return True


class NewTask(SystemCall):
    """System call to create new task from target coroutine"""

    def __init__(self, target: Coroutine) -> None:
        self.target = target

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        task_id = scheduler.new(self.target)
        task.set_syscall_result(task_id)
        return True


class KillTask(SystemCall):
    """System call to kill task with particular task id"""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        to_kill = scheduler.task_map.get(self.task_id)
        if to_kill:
            to_kill.is_running = False
            to_kill.target.close()
            task.set_syscall_result(scheduler.exit_task(self.task_id))
        else:
            task.set_syscall_result(False)
        return True


class WaitTask(SystemCall):
    """System call to wait task with particular task id"""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id

    def handle(self, scheduler: Scheduler, task: Task) -> bool:
        # Note: One shouldn't reschedule task which is waiting for another one.
        # But one must reschedule task if task id to wait for is invalid.
        result = scheduler.wait_task(task.task_id, self.task_id)
        task.set_syscall_result(result)
        return not result
