"""General shared utilities."""
import logging
from itertools import tee
from typing import Iterable, Any, Tuple
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest  # type: ignore


# Do not update the version manually - it is managed by `bumpversion`.
__version__: str = '3.0.1rc'
log = logging.getLogger(__name__)


def is_blank(string: str) -> bool:
    """Return True iff the string contains only whitespaces."""
    return not string.strip()


def pairwise(
    iterable: Iterable,
    default_value: Any,
) -> Iterable[Tuple[Any, Any]]:
    """Return pairs of items from `iterable`.

    pairwise([1, 2, 3], default_value=None) -> (1, 2) (2, 3), (3, None)
    """
    a, b = tee(iterable)
    _ = next(b, default_value)
    return zip_longest(a, b, fillvalue=default_value)
