# import importlib
# import pkgutil
# from fastapi import APIRouter
#
# from apps.app.api.routes import hello, tmall
#
# router = APIRouter()

# for module_finder, name, is_pkg in pkgutil.walk_packages(__path__):
#     if not is_pkg:
#         lib = importlib.import_module(f'apps.app.api.routes.{name}')
#         try:
#             sub_router = getattr(lib, 'router')
#             router.include_router(sub_router, tags=[f"{name}"], prefix=f"/{name}")
#         except AttributeError as e:
#             print(e)
