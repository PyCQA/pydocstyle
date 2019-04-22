"""Parsed source code checkers for docstring violations."""

import tokenize as tk

from pydocstyle import violations
from pydocstyle.checkers import get_checkers
from pydocstyle.config import IllegalConfiguration
from pydocstyle.parser import Parser, StringIO, ParseError, AllError
from pydocstyle.utils import log


__all__ = ('check', )


class ConventionChecker:
    """Checker for PEP 257 and numpy conventions.

    D10x: Missing docstrings
    D20x: Whitespace issues
    D30x: Docstring formatting
    D40x: Docstring content issues

    """

    def check_source(self, source, filename, ignore_decorators=None):
        yield from check_source(source, filename, ignore_decorators=ignore_decorators)

    @property
    def checks(self):
        return _get_checks()


def _get_checks():
    all = [this_check for this_check in get_checkers()
            if hasattr(this_check, '_check_for')]
    return sorted(all, key=lambda this_check: not this_check._terminal)


def check_source(source, filename, ignore_decorators=None):
    """Checker for PEP 257 and numpy conventions.

    D10x: Missing docstrings
    D20x: Whitespace issues
    D30x: Docstring formatting
    D40x: Docstring content issues

    """
    module = parse(StringIO(source), filename)
    for definition in module:
        for this_check in _get_checks():
            terminate = False
            if isinstance(definition, this_check._check_for):
                skipping_all = (definition.skipped_error_codes == 'all')
                decorator_skip = ignore_decorators is not None and any(
                    len(ignore_decorators.findall(dec.name)) > 0
                    for dec in definition.decorators)
                if not skipping_all and not decorator_skip:
                    error = this_check(definition,
                                        definition.docstring)
                else:
                    error = None
                errors = error if hasattr(error, '__iter__') else [error]
                for error in errors:
                    if error is not None and error.code not in \
                            definition.skipped_error_codes:
                        partition = this_check.__doc__.partition('.\n')
                        message, _, explanation = partition
                        error.set_context(explanation=explanation,
                                            definition=definition)
                        yield error
                        if this_check._terminal:
                            terminate = True
                            break
            if terminate:
                break


parse = Parser()


def check(filenames, select=None, ignore=None, ignore_decorators=None):
    """Generate docstring errors that exist in `filenames` iterable.

    By default, the PEP-257 convention is checked. To specifically define the
    set of error codes to check for, supply either `select` or `ignore` (but
    not both). In either case, the parameter should be a collection of error
    code strings, e.g., {'D100', 'D404'}.

    When supplying `select`, only specified error codes will be reported.
    When supplying `ignore`, all error codes which were not specified will be
    reported.

    Note that ignored error code refer to the entire set of possible
    error codes, which is larger than just the PEP-257 convention. To your
    convenience, you may use `pydocstyle.violations.conventions.pep257` as
    a base set to add or remove errors from.

    Examples
    ---------
    >>> check(['pydocstyle.py'])
    <generator object check at 0x...>

    >>> check(['pydocstyle.py'], select=['D100'])
    <generator object check at 0x...>

    >>> check(['pydocstyle.py'], ignore=conventions.pep257 - {'D100'})
    <generator object check at 0x...>

    """
    if select is not None and ignore is not None:
        raise IllegalConfiguration('Cannot pass both select and ignore. '
                                   'They are mutually exclusive.')
    elif select is not None:
        checked_codes = select
    elif ignore is not None:
        checked_codes = list(set(violations.ErrorRegistry.get_error_codes()) -
                             set(ignore))
    else:
        checked_codes = violations.conventions.pep257

    for filename in filenames:
        log.info('Checking file %s.', filename)
        try:
            with tk.open(filename) as file:
                source = file.read()
            for error in check_source(source, filename, ignore_decorators):
                code = getattr(error, 'code', None)
                if code in checked_codes:
                    yield error
        except (EnvironmentError, AllError, ParseError) as error:
            log.warning('Error in file %s: %s', filename, error)
            yield error
        except tk.TokenError:
            yield SyntaxError('invalid syntax in file %s' % filename)
