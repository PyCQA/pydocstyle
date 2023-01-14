"""This module contains the convention definitions."""

from typing import Set

from typing_extensions import Literal

from pydocstyle.violations import all_errors

CONVENTION_NAMES = ("pep257", "numpy", "google")


convention_errors = {
    'pep257': all_errors
    - {
        'D203',
        'D212',
        'D213',
        'D214',
        'D215',
        'D404',
        'D405',
        'D406',
        'D407',
        'D408',
        'D409',
        'D410',
        'D411',
        'D413',
        'D415',
        'D416',
        'D417',
        'D418',
    },
    'numpy': all_errors
    - {
        'D107',
        'D203',
        'D212',
        'D213',
        'D402',
        'D413',
        'D415',
        'D416',
        'D417',
    },
    'google': all_errors
    - {
        'D203',
        'D204',
        'D213',
        'D215',
        'D400',
        'D401',
        'D404',
        'D406',
        'D407',
        'D408',
        'D409',
        'D413',
    },
}


class Convention:
    """This class defines the convention to use for checking docstrings."""

    def __init__(
        self, name: Literal["pep257", "numpy", "google"] = "pep257"
    ) -> None:
        """Initialize the convention.

        The convention has two purposes. First, it holds the error codes to be
        checked. Second, it defines how to treat docstrings, eliminating the
        need for extra logic to determine whether a docstring is a NumPy or
        Google style docstring.

        Each convention has a set of error codes to check as a baseline.
        Specific error codes can be added or removed via the
        :code:`add_error_codes` or :codes:`remove_error_codes` methods.

        Args:
            name (Literal["pep257", "numpy", "google"], optional): The convention to use. Defaults to "pep257".

        Raises:
            ValueError: _description_
        """
        if name not in CONVENTION_NAMES:
            name = "pep257"

        self.name = name
        self.error_codes = convention_errors[name]

    def add_error_codes(self, error_codes: Set[str]) -> None:
        """Add additional error codes to the convention.

        Args:
            error_codes (Set[str]): The error codes to also check.
        """
        self.error_codes = self.error_codes.union(error_codes)

    def remove_error_codes(self, error_codes: Set[str]) -> None:
        """Remove error codes from the convention.

        Args:
            error_codes (Set[str]): The error codes to ignore.
        """
        self.error_codes = self.error_codes - error_codes
