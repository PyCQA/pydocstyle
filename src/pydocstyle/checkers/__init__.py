from pydocstyle.checkers.hooks import get_checkers
# These imports below are required for registering the
# checkers so that `get_checkers` captures them.
from pydocstyle.checkers.style import numpy, base, other

__all__ = ('get_checkers', 'numpy', 'base', 'other')
