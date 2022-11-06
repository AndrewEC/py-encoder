import math
from typing import Callable
import threading
from time import sleep
import ctypes


class TestCaseThread(threading.Thread):

    def __init__(self, function: Callable, *args, **kwargs):
        super().__init__()
        self._function = function
        self._args = args
        self._kwargs = kwargs
        self._running = False
        self._lock = threading.Lock()
        self.execution_exception = None

    def run(self) -> None:
        self._running = True
        self._set_running(True)
        try:
            self._function(*self._args, **self._kwargs)
        except Exception as e:
            self.execution_exception = e
        self._set_running(False)

    def _set_running(self, value: bool):
        with self._lock:
            self._running = value

    def is_running(self) -> bool:
        with self._lock:
            return self._running


class TimeoutThread(threading.Thread):

    _WAIT_TIME = 0.25

    def __init__(self, execution_timeout: int, function: Callable, *args, **kwargs):
        super().__init__()
        self.execution_exception = None
        self._execution_timeout = execution_timeout
        self._test_case_thread = TestCaseThread(function, *args, **kwargs)
        self._wait_iterations = math.floor(int(execution_timeout / TimeoutThread._WAIT_TIME))

    def run(self) -> None:
        self._test_case_thread.start()
        for _ in range(self._wait_iterations):
            if not self._test_case_thread.is_running():
                break
            sleep(TimeoutThread._WAIT_TIME)
        if self._test_case_thread.is_running():
            try:
                self._force_quit_test_case_thread()
                self.execution_exception = SystemError(f'Test case thread did not complete in the allotted [{self._execution_timeout}] seconds.')
            except Exception as e:
                self.execution_exception = e
        else:
            self._test_case_thread.join()

    def _force_quit_test_case_thread(self):
        print(f'Test case timeout, attempting to force close test case thread: [{self._test_case_thread.ident}]')
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self._test_case_thread.ident), exc)
        if res == 0:
            raise ValueError("Could not stop test case thread. Non-existent thread id.")
        elif res > 1:
            # If it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect.
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self._test_case_thread.ident, None)
            raise SystemError("An issue occurred while stopping test case thread. PyThreadState_SetAsyncExc failed")

    def has_exception(self):
        return self.get_exception() is not None

    def get_exception(self) -> Exception | None:
        return self.execution_exception if self.execution_exception is not None else self._test_case_thread.execution_exception


def timeout(timeout_seconds: int):
    """
    This exists to resolve an issue in the mutmut mutation testing framework. Mutmut opens a subprocess to execute
    the unit test suite after applying a mutation. However, if the mutation causes an infinite loop the mutmut process
    seems to get stuck and can't properly close the subprocess causing the mutation test execution to hang indefinitely.

    This will raise an exception which will cause the unit test to fail when the specified timeout period has elapsed.
    """
    def inner(function):
        def wrapper(*args, **kwargs):
            timeout_thread = TimeoutThread(timeout_seconds, function, *args, **kwargs)
            timeout_thread.start()
            timeout_thread.join()
            if timeout_thread.has_exception():
                raise timeout_thread.get_exception()
        return wrapper
    return inner
