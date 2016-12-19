class Expectation(object):
    """Hold expectation for pep257 violations in tests."""

    def __init__(self):
        self.expected = set()

    def expect(self, *args):
        """Decorator that expects a certain PEP 257 violation."""
        def none(_):
            return None

        if len(args) == 1:
            return lambda f: (self.expected.add((f.__name__, args[0])) or
                              none(f()) or f)
        self.expected.add(args)
