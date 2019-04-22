import pkg_resources

from typing import Set

from pydocstyle.utils import log

__registered_checkers = []
__loaded_styles = set()  # type: Set[str]

ENTRY_POINT_NAME = 'pydocstyle_styles'


def check_for(kind, terminal=False):
    def decorator(f):
        __registered_checkers.append(f)
        f._check_for = kind
        f._terminal = terminal
        return f
    return decorator


def _load_styles():
    for entry_point in pkg_resources.iter_entry_points(ENTRY_POINT_NAME):
        if entry_point.name not in __loaded_styles:
            try:
                entry_point.load()
            except Exception as error:
                log.exception("Unable to load plugin %s.\nError occurred: %s",
                              entry_point.name, error)
            else:
                __loaded_styles.add(entry_point.name)


def get_checkers():
    _load_styles()
    return  iter(__registered_checkers)
