import abc
import asyncio
import time
from typing import List


class AbstractRetryStrategy(abc.ABC):
    _initial_timeout: int
    _retries: int
    timeouts: List[int]

    def __init__(self, initial_timeout: int, retries: int):
        self._initial_timeout = initial_timeout
        self._retries = retries
        self.timeouts = self.get_timeouts()
        self.timeouts.append(None)

    def __call__(self):
        for i in self.timeouts:
            yield i

    @abc.abstractmethod
    def get_timeouts(self):
        """List of timeouts generated by implementation classes.
        """
        ...


class LinearRetryStrategy(AbstractRetryStrategy):
    def __init__(self, initial_timeout: int, retries: int):
        super().__init__(initial_timeout, retries)

    def get_timeouts(self):
        return list(range(self._initial_timeout, self._initial_timeout * self._retries + 1, self._initial_timeout))


class ExponentialRetryStrategy(AbstractRetryStrategy):
    _factor: int

    def __init__(self, initial_timeout: int, retries: int, factor: int):
        self._factor = factor
        super().__init__(initial_timeout, retries)

    def get_timeouts(self):
        timeouts = [self._initial_timeout]

        for _ in range(1, self._retries):
            timeouts.append(timeouts[-1] * self._factor)

        return timeouts