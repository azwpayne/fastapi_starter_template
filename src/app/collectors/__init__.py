import importlib
import os
from os.path import dirname
from pkgutil import iter_modules

from fastapi import APIRouter

router = APIRouter()

collection_path = dirname(__file__)

for root, dirs, files in os.walk(collection_path):
    relative_path = os.path.relpath(root, collection_path)
    module_root = '.'.join(relative_path.split(os.sep)) if relative_path != '.' else ''
    for _, module_name, is_pkg in iter_modules([root]):
        if not is_pkg:
            full_module_path = f'src.app.collectors.{module_root}.{module_name}' if module_root else f'src.app.collectors.{module_name}'
            lib = importlib.import_module(full_module_path)
            sub_router = getattr(lib, 'router', None)
            if sub_router:
                url_prefix = f'/{relative_path}/{module_name}'.rstrip(
                    '__pycache__') if relative_path else f'/{module_name}'
                router.include_router(sub_router, prefix=url_prefix.replace("./", "").rstrip('/'))
