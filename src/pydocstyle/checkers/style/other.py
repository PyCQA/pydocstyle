import ast

from pydocstyle import violations
from pydocstyle.parser import Definition
from pydocstyle.checkers.hooks import check_for


@check_for(Definition)
def check_multi_line_summary_start(definition, docstring):
    """D21{2,3}: Multi-line docstring summary style check.

    A multi-line docstring summary should start either at the first,
    or separately at the second line of a docstring.

    """
    if docstring:
        start_triple = [
            '"""', "'''",
            'u"""', "u'''",
            'r"""', "r'''",
            'ur"""', "ur'''"
        ]

        lines = ast.literal_eval(docstring).split('\n')
        if len(lines) > 1:
            first = docstring.split("\n")[0].strip().lower()
            if first in start_triple:
                return violations.D212()
            else:
                return violations.D213()
