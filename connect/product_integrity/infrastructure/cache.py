import os
import time
from typing import Optional

import jsonpickle

from connect.product_integrity.infrastructure.contracts import Cache


class FileSystemCache(Cache):
    def __init__(self, file_path: str, ttl: int = 86400):
        self.file_path = file_path.strip().rstrip('/')
        self.ttl = ttl

    def _get_file_name(self, id: str) -> str:
        return f'{self.file_path}/connect.{id}.cache.json'

    def _has_cache_expired(self, id: str) -> bool:
        return int(time.time() - os.path.getmtime(self._get_file_name(id))) >= self.ttl

    def put(self, id: str, content: object):
        print('save into cache')
        with open(self._get_file_name(id), 'w') as cache:
            cache.write(jsonpickle.encode(content))

    def get(self, id: str) -> Optional[object]:
        try:
            if self._has_cache_expired(id):
                os.remove(self._get_file_name(id))

            with open(self._get_file_name(id), 'r') as cache:
                return jsonpickle.decode(cache.read())
        except FileNotFoundError:
            return None
