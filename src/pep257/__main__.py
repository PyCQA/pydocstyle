import sys
from . import run_pep257


def main():
    try:
        sys.exit(run_pep257())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
