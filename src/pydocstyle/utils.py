"""General shared utilities."""
import collections
import logging
import re
import io
import sys
import tokenize
from typing import Callable, DefaultDict, Iterable, Any, Tuple
from itertools import tee, zip_longest

DIFF_HUNK_REGEXP = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@.*$")


# Do not update the version manually - it is managed by `bumpversion`.
__version__ = '3.0.1rc'
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
    _ = next(b, default_value)  # noqa: F841
    return zip_longest(a, b, fillvalue=default_value)


def _stdin_get_value_py3() -> io.StringIO:
    stdin_value = sys.stdin.buffer.read()
    fd = io.BytesIO(stdin_value)
    try:
        (coding, lines) = tokenize.detect_encoding(fd.readline)
        return io.StringIO(stdin_value.decode(coding))
    except (LookupError, SyntaxError, UnicodeError):
        return io.StringIO(stdin_value.decode("utf-8"))


def stdin_get_value():
    # type: () -> str
    """Get and cache it so plugins can use it."""
    cached_value = getattr(stdin_get_value, "cached_stdin", None)
    if cached_value is None:
        if sys.version_info < (3, 0):
            stdin_value = io.BytesIO(sys.stdin.read())
        else:
            stdin_value = _stdin_get_value_py3()
        stdin_get_value.cached_stdin = stdin_value  # type: ignore
        cached_value = stdin_get_value.cached_stdin  # type: ignore
    return cached_value.getvalue()


def parse_unified_diff(diff: str = None) -> DefaultDict:
    """Parse the unified diff passed on stdin.

    :returns:
        dictionary mapping file names to sets of line numbers
    :rtype:
        dict
    """
    # Allow us to not have to patch out stdin_get_value
    if diff is None:
        diff = stdin_get_value()

    number_of_rows = None
    current_path = None
    parsed_paths = collections.defaultdict(set)  # type: DefaultDict
    for line in diff.splitlines():
        if number_of_rows:
            # NOTE(sigmavirus24): Below we use a slice because stdin may be
            # bytes instead of text on Python 3.
            if line[:1] != "-":
                number_of_rows -= 1
            # We're in the part of the diff that has lines starting with +, -,
            # and ' ' to show context and the changes made. We skip these
            # because the information we care about is the filename and the
            # range within it.
            # When number_of_rows reaches 0, we will once again start
            # searching for filenames and ranges.
            continue

        # NOTE(sigmavirus24): Diffs that we support look roughly like:
        #    diff a/file.py b/file.py
        #    ...
        #    --- a/file.py
        #    +++ b/file.py
        # Below we're looking for that last line. Every diff tool that
        # gives us this output may have additional information after
        # ``b/file.py`` which it will separate with a \t, e.g.,
        #    +++ b/file.py\t100644
        # Which is an example that has the new file permissions/mode.
        # In this case we only care about the file name.
        if line[:3] == "+++":
            current_path = line[4:].split("\t", 1)[0]
            # NOTE(sigmavirus24): This check is for diff output from git.
            if current_path[:2] == "b/":
                current_path = current_path[2:]
            # We don't need to do anything else. We have set up our local
            # ``current_path`` variable. We can skip the rest of this loop.
            # The next line we will see will give us the hung information
            # which is in the next section of logic.
            continue

        hunk_match = DIFF_HUNK_REGEXP.match(line)
        # NOTE(sigmavirus24): pep8/pycodestyle check for:
        #    line[:3] == '@@ '
        # But the DIFF_HUNK_REGEXP enforces that the line start with that
        # So we can more simply check for a match instead of slicing and
        # comparing.
        if hunk_match:
            (row, number_of_rows) = [
                1 if not group else int(group)
                for group in hunk_match.groups()
            ]
            parsed_paths[current_path].update(
                range(row, row + number_of_rows)
            )

    # We have now parsed our diff into a dictionary that looks like:
    #    {'file.py': set(range(10, 16), range(18, 20)), ...}
    __import__('wdb').set_trace()
    return parsed_paths
