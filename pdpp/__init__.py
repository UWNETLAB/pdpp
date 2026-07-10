from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("pdpp")
except PackageNotFoundError:  # pragma: no cover - not installed as a package
    __version__ = "0.0.0"
