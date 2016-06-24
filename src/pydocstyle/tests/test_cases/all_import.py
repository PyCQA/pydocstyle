"""A valid module docstring."""

from .all_import_aux import __all__
from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


@expect("D103: Missing docstring in public function")
def public_func():
    pass


@expect("D103: Missing docstring in public function")
def this():
    pass
