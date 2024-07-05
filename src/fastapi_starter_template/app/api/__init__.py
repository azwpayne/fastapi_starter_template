import importlib
import os
from os.path import dirname, basename, join
from pkgutil import iter_modules

from fastapi import APIRouter

router = APIRouter()


def add_router(router_folder, router_name):
    try:
        lib = importlib.import_module(f"src.fastapi_starter_template.app.api.{router_folder}.{module_name}")
        sub_router = getattr(lib, 'router')
        router.include_router(sub_router, prefix=f"/{router_folder}/{router_name}")
    except AttributeError:
        pass


for i in os.listdir(dirname(__file__)):
    for module_path, module_name, is_pkg in iter_modules([join(dirname(__file__), i)]):
        if not is_pkg:
            add_router(basename(module_path.path), module_name)
