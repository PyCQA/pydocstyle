class Expectation:
    """Hold expectation for pep257 violations in tests."""

    def __init__(self):
        self.expected = set()

    def expect(self, *args, arg_count=0, func_name=""):
        """Decorator that expects a certain PEP 257 violation."""
        # The `arg_count` parameter helps the decorator
        # with functions that have positional arguments.
        if len(args) == 1:
            def decorate(f):
                self.expected.add((func_name or f.__name__, args[0]))
                f(*[None]*arg_count)
                return f
            return decorate
        self.expected.add(args)
