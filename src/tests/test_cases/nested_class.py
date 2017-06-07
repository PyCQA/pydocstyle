"""A valid module docstring."""

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect

expect('PublicClass', 'D101: Missing docstring in public class')


class PublicClass(object):

    expect('PublicNestedClass',
           'D106: Missing docstring in public nested class')

    class PublicNestedClass(object):

        expect('PublicNestedClassInPublicNestedClass',
               'D106: Missing docstring in public nested class')

        class PublicNestedClassInPublicNestedClass(object):
            pass

        class _PrivateNestedClassInPublicNestedClass(object):
            pass

    class _PrivateNestedClass(object):

        class PublicNestedClassInPrivateNestedClass(object):
            pass

        class _PrivateNestedClassInPrivateNestedClass(object):
            pass
