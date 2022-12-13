from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Iterable, Optional

from connect.product_integrity.domain.models import ProductID, Product


class ProductSource(metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def id(self) -> str:
        pass

    @abstractmethod
    def parameters(self) -> Iterable[Dict[str, Any]]:
        pass


class ProductRepository(metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def find(self, id: ProductID) -> Optional[Product]:
        pass
