from typing import List

from connect.product_integrity.domain.contracts import ProductRepository
from connect.product_integrity.domain.exceptions import UnsupportedProduct, InvalidProductParameters
from connect.product_integrity.domain.models import Product, ProductID

UNSUPPORTED_PRODUCT_BY_DEVOPS = 'Unsupported product {id}, this DevOps services supports {supported}.'
UNSUPPORTED_PRODUCT_BY_PLATFORM = 'Unsupported product {id}, unable to find product definition in Connect Platform.'
MISSING_PRODUCT_PARAMETERS = 'Missing or not compliant parameters in product definition in connect Platform {missing}.'


class ProductDefinitionChecker:
    def __init__(self, products: List[Product], repository: ProductRepository):
        self.products = products
        self.repository = repository

    def __call__(self, id: ProductID):
        self.check(id)

    def check(self, id: ProductID):
        # 1. check if the product is in the supported list of products.
        try:
            schema = next(filter(lambda prd: prd.id == id, self.products))
        except StopIteration:
            raise UnsupportedProduct(UNSUPPORTED_PRODUCT_BY_DEVOPS.format(
                id=id,
                supported=", ".join(list(map(lambda prd: prd.id.value, self.products))),
            ), id)

        # 2. fetch the product definition from API.
        product = self.repository.find(id)
        if product is None:
            raise UnsupportedProduct(UNSUPPORTED_PRODUCT_BY_PLATFORM.format(
                id=id,
            ), id)

        # 3. match the list of parameters.
        missing = schema.parameter_difference(product)
        if len(missing) > 0:
            raise InvalidProductParameters(MISSING_PRODUCT_PARAMETERS.format(
                missing=missing,
            ), id, missing)
