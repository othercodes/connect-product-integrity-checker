from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re


@dataclass
class ProductID:
    value: str

    def __post_init__(self):
        self._must_have_valid_format()

    def _must_have_valid_format(self):
        pattern = '^PRD(-\d{3}){3}$'
        if re.match(pattern, self.value) is None:
            raise ValueError(f'Invalid product id {self.value} format must match {pattern} pattern.')

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(value={self.value})'


@dataclass
class Parameter:
    name: str
    type: str
    scope: str
    phase: str
    constraints: dict


class Product:
    def __init__(self, id: ProductID, parameters: List[Parameter]):
        self.id = id
        self.parameters = parameters

    def __hash__(self) -> int:
        return hash(self.id.value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False

        return self.id == other.id

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id}, parameters={self.parameters})'

    def parameter_difference(self, other: Product) -> List[Parameter]:
        return [item for item in self.parameters if item not in other.parameters]
