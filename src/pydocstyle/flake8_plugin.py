"""Flake8 plugin."""

from .config import ConfigurationParser
from .checker import check
from .utils import __version__


class Checker:
    """Flake8 pydocstyle checker."""
    name = 'pydocstyle'
    version = __version__

    def __init__(self, tree, filename):
        _ = tree  # Without tree in the signature, we're not instantiated.
        self.config = ConfigurationParser()
        self.config.parse([filename])

    def run(self):
        """Run checker for filename it was initialized with."""
        ((filename, checked_codes, ignore_decorators),) = list(self.config.get_files_to_check())
        for error in check((filename,), select=checked_codes, ignore_decorators=ignore_decorators):
            yield (error.line, 0, error.message.replace(':', '', 1), type(error))
