import importlib
import pkgutil


def import_packages(path: list[str], package: str) -> None:
    for _, module_name, is_pkg in pkgutil.iter_modules(path):
        if not is_pkg:
            continue
        subpackage = f"{package}.{module_name}"
        importlib.import_module(subpackage)
