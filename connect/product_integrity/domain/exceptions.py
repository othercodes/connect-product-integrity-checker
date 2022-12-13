from typing import List

from connect.product_integrity.domain.models import ProductID, Parameter


class ProductDefinitionFailure(Exception):
    def __init__(self, message: str, product_id: ProductID):
        super().__init__(message)

        self.product_id = product_id


class UnsupportedProduct(ProductDefinitionFailure):
    pass


class InvalidProductParameters(ProductDefinitionFailure):
    def __init__(self, message: str, product_id: ProductID, parameters: List[Parameter]):
        super().__init__(message, product_id)

        self.parameters = parameters
