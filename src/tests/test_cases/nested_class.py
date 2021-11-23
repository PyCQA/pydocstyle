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

        expect('_PrivateNestedClassInPublicNestedClass',
               'D156: Missing docstring in private nested class')

        class _PrivateNestedClassInPublicNestedClass:
            pass

    expect('_PrivateNestedClass',
            'D156: Missing docstring in private nested class')

    class _PrivateNestedClass:

        expect('PublicNestedClassInPrivateNestedClass',
               'D156: Missing docstring in private nested class')

        class PublicNestedClassInPrivateNestedClass:
            pass

        expect('_PrivateNestedClassInPrivateNestedClass',
               'D156: Missing docstring in private nested class')

        class _PrivateNestedClassInPrivateNestedClass:
            pass
