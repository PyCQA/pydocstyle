"""General shared utilities."""
import logging
from typing import Iterable, Any, Tuple
from itertools import tee, zip_longest


# Do not update the version manually - it is managed by `bumpversion`.
__version__ = "4.0.1"
log = logging.getLogger(__name__)


def is_blank(string: str) -> bool:
    """Return True iff the string contains only whitespaces."""
    return not string.strip()


def pairwise(
    iterable: Iterable, default_value: Any
) -> Iterable[Tuple[Any, Any]]:
    """Return pairs of items from `iterable`.

    pairwise([1, 2, 3], default_value=None) -> (1, 2) (2, 3), (3, None)
    """
    a, b = tee(iterable)
    _ = next(b, default_value)
    return zip_longest(a, b, fillvalue=default_value)


def common_prefix_length(a: str, b: str) -> int:
    """Return the length of the longest common prefix of a and b.

    >>> common_prefix_length('abcd', 'abce')
    3

    """
    for common, (ca, cb) in enumerate(zip(a, b)):
        if ca != cb:
            return common
    return min(len(a), len(b))
