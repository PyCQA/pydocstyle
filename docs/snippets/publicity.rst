The D1xx group of errors deals with missing docstring in public constructs:
modules, classes, methods, etc. It is important to note how publicity is
determined and what its effects are.


How publicity is determined
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Publicity for all constructs is determined as follows: a construct is
considered *public* if -

1. Its immediate parent is public *and*
2. Its name does not contain a single leading underscore.

A construct's immediate parent is the construct that contains it. For example,
a method's parent is a class object. A class' parent is usually a module, but
might also be a function, method, etc. A module can either have no parent, or
it can have a parent that is a package.

In order for a construct to be considered public, its immediate parent must
also be public. Since this definition is recursive, it means that *all* of its
parents need to be public. The corollary is that if a construct is considered
private, then all of its descendants are also considered private. For example,
a class called ``_Foo`` is considered private. A method ``bar`` in ``_Foo`` is
also considered private since its parent is a private class, even though its
name does not begin with a single underscore.

Modules are parsed to look if ``__all__`` is defined. If so, only those top
level constructs are considered public. The parser looks for ``__all__``
defined as a literal list or tuple. As the parser doesn't execute the module,
any mutation of ``__all__`` will not be considered.


How publicity affects error reports
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The immediate effect of a construct being determined as private is that no
D1xx errors will be reported for it (or its children, as the previous section
explains). A private method, for instance, will not generate a D102 error, even
if it has no docstring.

However, it is important to note that while docstring are optional for private
construct, they are still required to adhere to your style guide. So if a
private module `_foo.py` does not have a docstring, it will not generate a
D100 error, but if it *does* have a docstring, that docstring might generate
other errors.
