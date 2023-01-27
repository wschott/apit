import pkgutil


def import_packages(path: list[str]) -> None:
    for loader, module_name, is_pkg in pkgutil.iter_modules(path):
        if not is_pkg:
            continue
        _module = loader.find_module(module_name).load_module(module_name)  # type: ignore
        globals()[module_name] = _module
