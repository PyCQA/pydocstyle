from pydocstyle.checker import check, check_source
from pydocstyle.violations import Error, conventions
from pydocstyle.utils import __version__

# Temporary hotfix for flake8-docstrings
from pydocstyle.checker import ConventionChecker
from pydocstyle.parser import AllError
