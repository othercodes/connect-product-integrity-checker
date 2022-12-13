from typing import Dict, Any, Iterable, Optional

from connect.client import ConnectClient, ClientError

from connect.product_integrity.domain.contracts import ProductSource, ProductRepository
from connect.product_integrity.domain.models import ProductID, Product
from connect.product_integrity.domain.services import product_builder
from connect.product_integrity.infrastructure.contracts import Cache


class ConnectProductSource(ProductSource):
    def __init__(self, product: dict):
        self.product = product

    def id(self) -> str:
        return self.product.get('id')

    def parameters(self) -> Iterable[Dict[str, Any]]:
        for parameter in self.product.get('parameters', []):
            yield {
                'name': parameter.get('name'),
                'type': parameter.get('type'),
                'scope': parameter.get('scope'),
                'phase': parameter.get('phase'),
                'constraints': parameter.get('constraints'),
            }


class ConnectProductRepository(ProductRepository):
    def __init__(self, client: ConnectClient, cache: Optional[Cache] = None):
        self.client = client
        self.cache = cache

    def find(self, id: ProductID) -> Optional[Product]:
        product = self.cache.get(id.value)  # type: Optional[Product]
        if product is not None:
            return product

        try:
            dictionary = self.client.products[id.value].get()
            dictionary['parameters'] = list(self.client.products[id.value].parameters.all())
            product = product_builder(ConnectProductSource(dictionary))

            self.cache.put(product.id.value, product)
        except ClientError as e:
            if e.status_code == 404:
                return None
            raise

        return product
