__registered_checkers = []

def check_for(kind, terminal=False):
    def decorator(f):
        __registered_checkers.append(f)
        f._check_for = kind
        f._terminal = terminal
        return f
    return decorator


def get_checkers():
    return  iter(__registered_checkers)
