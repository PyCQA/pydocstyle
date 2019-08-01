"""A valid module docstring."""


from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


@expect('D103: Missing docstring in public function')
def public_function():

    @expect("D417: Missing arguments in the function docstring "
            "(argument(s) 'y' missing in function "
            "'test_nested_missing_args' docstring)")
    def test_nested_missing_args(x=1, y=2):  # noqa: D213, D407, D413
        """Do something.

        Args:
            x : An argument.
        """
        pass

    def test_nested_ok(x=1):  # noqa: D213, D407, D413
        """Do something.

        Args:
            x : An argument.
        """
        pass

        def test_nested_in_nested_ok(x=1, y=2):  # noqa: D213, D407, D413
            """Do something.

            Args:
                x : An argument.
                y : Another argument.
            """
            pass

        @expect("D417: Missing arguments in the function docstring "
                "(argument(s) 'z' missing in function "
                "'test_nested_in_nested_missing_args' docstring)")
        def test_nested_in_nested_missing_args(x=1, z=2):  # noqa: D213, D407, D413
            """Do something.

            Args:
                x : An argument.
            """
            pass
    return test_nested_ok


public_function()()
