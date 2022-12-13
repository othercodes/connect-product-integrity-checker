from abc import ABCMeta, abstractmethod
from typing import Optional


class Cache(metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def put(self, id: str, content: object):
        pass

    @abstractmethod
    def get(self, id: str) -> Optional[object]:
        pass
