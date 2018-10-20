"""A valid module docstring."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect

expect('PublicClass', 'D101: Missing docstring in public class')


class PublicClass:

    expect('PublicNestedClass',
           'D106: Missing docstring in public nested class')

    class PublicNestedClass:

        expect('PublicNestedClassInPublicNestedClass',
               'D106: Missing docstring in public nested class')

        class PublicNestedClassInPublicNestedClass:
            pass

        class _PrivateNestedClassInPublicNestedClass:
            pass

    class _PrivateNestedClass:

        class PublicNestedClassInPrivateNestedClass:
            pass

        class _PrivateNestedClassInPrivateNestedClass:
            pass
