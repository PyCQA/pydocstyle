"""Examples from the pep257 specification."""

# Examples from the official "Python PEP 257 -- Docstring Conventions"
# documentation:
#     * As HTML: https://www.python.org/dev/peps/pep-0257
#     * Source reST: https://github.com/python/peps/blob/master/pep-0257.txt

from .expected import Expectation

expectation = Expectation()
expect = expectation.expect


# "One-line Docstrings" section example
# https://www.python.org/dev/peps/pep-0257/#id16
def kos_root():
    """Return the pathname of the KOS root directory."""
    global _kos_root
    if _kos_root:
        return _kos_root


# "Multiline-line Docstrings" section example
# https://www.python.org/dev/peps/pep-0257/#id17
@expect("D213: Multi-line docstring summary should start at the second line")
@expect("D405: Section name should be properly capitalized "
        "('Keyword Arguments', not 'Keyword arguments')")
@expect("D407: Missing dashed underline after section ('Keyword Arguments')")
@expect("D413: Missing blank line after last section ('Keyword Arguments')")
def complex(real=0.0, imag=0.0):
    """Form a complex number.

    Keyword arguments:
    real -- the real part (default 0.0)
    imag -- the imaginary part (default 0.0)
    """
    if imag == 0.0 and real == 0.0:
        complex_zero = 0  # added to avoid NameError with @expect decorator
        return complex_zero
