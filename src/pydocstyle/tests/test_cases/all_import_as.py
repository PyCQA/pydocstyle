"""A valid module docstring."""

from .all_import_aux import __all__ as not_dunder_all
from .expected import Expectation

expectation = Expectation()
expect = expectation.expect

__all__ = ('public_func', )


@expect("D103: Missing docstring in public function")
def public_func():
    pass


def private_func():
    pass
