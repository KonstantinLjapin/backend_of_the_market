import importlib
import pkgutil
from fastapi import APIRouter
from pathlib import Path


def load_routers_from_package(package_name: str) -> APIRouter:
    """
    Загружает и включает все APIRouter из указанного пакета по имени.
    Пример: load_routers_from_package("src.routers")
    """
    router = APIRouter()
    package = importlib.import_module(package_name)
    package_path = Path(package.__file__).parent

    for _, module_name, _ in pkgutil.iter_modules([str(package_path)]):
        full_name = f"{package_name}.{module_name}"
        module = importlib.import_module(full_name)
        if hasattr(module, "router"):
            subrouter = getattr(module, "router")
            if isinstance(subrouter, APIRouter):
                router.include_router(subrouter)

    return router
