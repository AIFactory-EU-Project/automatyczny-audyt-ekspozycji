# see https://packaging.python.org/guides/packaging-namespace-packages/
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)