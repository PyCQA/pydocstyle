"""This module contains tests for the available conventions."""

import re

import pytest

from pydocstyle.conventions import CONVENTION_NAMES, Convention


def test_default_convention_is_pep257() -> None:
    """Test that pep257 is used as the default convention."""
    convention = Convention()

    assert convention.name == "pep257"

    convention = Convention("invalid_convention")

    assert convention.name == "pep257"


@pytest.mark.parametrize("convention_name", CONVENTION_NAMES)
def test_names_are_set_correctly(convention_name: str) -> None:
    """Test that the convention holds its name as an attribute."""
    convention = Convention(convention_name)

    assert convention.name == convention_name


@pytest.mark.parametrize("convention_name", CONVENTION_NAMES)
def test_conventions_keep_their_error_codes_as_attribute(
    convention_name: str,
) -> None:
    """Check that conventions are initialized with a set of error codes."""
    convention = Convention(convention_name)

    assert len(convention.error_codes) > 0

    for error_code in convention.error_codes:
        assert len(error_code) == 4
        assert re.compile(r"D[1-4]\d\d").match(error_code)


def test_can_add_error_codes() -> None:
    """Test that additional error codes can be added to a convention."""
    convention = Convention()

    n_errors_before_adding = len(convention.error_codes)

    assert "D203" not in convention.error_codes
    assert "D212" not in convention.error_codes

    convention.add_error_codes({"D203", "D212"})

    assert len(convention.error_codes) - n_errors_before_adding == 2

    assert "D203" in convention.error_codes
    assert "D212" in convention.error_codes


def test_can_remove_error_codes() -> None:
    """Test that specific error codes can be removed from a convention."""
    convention = Convention()

    n_errors_before_removal = len(convention.error_codes)

    assert "D100" in convention.error_codes
    assert "D102" in convention.error_codes

    convention.remove_error_codes({"D100", "D102"})

    assert n_errors_before_removal - len(convention.error_codes) == 2

    assert "D100" not in convention.error_codes
    assert "D102" not in convention.error_codes
