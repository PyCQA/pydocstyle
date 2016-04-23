# -*- coding: utf-8 -*-
"""A module."""

from __future__ import unicode_literals
from .expected import Expectation


expectation = Expectation()
expect = expectation.expect


def with_unicode_docstring_without_u():
    r"""Check unicode: \u2611."""
