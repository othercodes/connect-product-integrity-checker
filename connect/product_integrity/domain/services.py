from typing import Dict, Any

from connect.product_integrity.domain.contracts import ProductSource
from connect.product_integrity.domain.models import Product, ProductID, Parameter


def product_builder(source: ProductSource) -> Product:
    def param_builder(source: Dict[str, Any]) -> Parameter:
        return Parameter(
            name=source['name'],
            type=source['type'],
            scope=source['scope'],
            phase=source['phase'],
            constraints=source['constraints'],
        )

    return Product(
        id=ProductID(source.id()),
        parameters=[param_builder(param) for param in source.parameters()]
    )
