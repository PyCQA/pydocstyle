import logging
import sys

from pydocstyle import log
from violations import Error
from config import ConfigurationParser, IllegalConfiguration
from checker import check


class ReturnCode(object):
    no_violations_found = 0
    violations_found = 1
    invalid_options = 2


def run_pydocstyle(use_pep257=False):
    log.setLevel(logging.DEBUG)
    conf = ConfigurationParser()
    setup_stream_handlers(conf.get_default_run_configuration())

    try:
        conf.parse()
    except IllegalConfiguration:
        return ReturnCode.invalid_options

    run_conf = conf.get_user_run_configuration()

    # Reset the logger according to the command line arguments
    setup_stream_handlers(run_conf)

    if use_pep257:
        log.warning("Deprecation Warning:\n"
                    "pep257 has been renamed to pydocstyle and the use of the "
                    "pep257 executable is deprecated and will be removed in "
                    "the next major version. Please use `pydocstyle` instead.")

    log.debug("starting in debug mode.")

    Error.explain = run_conf.explain
    Error.source = run_conf.source

    errors = []
    try:
        for filename, checked_codes in conf.get_files_to_check():
            errors.extend(check((filename,), select=checked_codes))
    except IllegalConfiguration:
        # An illegal configuration file was found during file generation.
        return ReturnCode.invalid_options

    code = ReturnCode.no_violations_found
    count = 0
    for error in errors:
        sys.stderr.write('%s\n' % error)
        code = ReturnCode.violations_found
        count += 1
    if run_conf.count:
        print(count)
    return code


def main(use_pep257=False):
    try:
        sys.exit(run_pydocstyle(use_pep257))
    except KeyboardInterrupt:
        pass


def main_pep257():
    main(use_pep257=True)


def setup_stream_handlers(conf):
    """Setup logging stream handlers according to the options."""
    class StdoutFilter(logging.Filter):
        def filter(self, record):
            return record.levelno in (logging.DEBUG, logging.INFO)

    log.handlers = []

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.WARNING)
    stdout_handler.addFilter(StdoutFilter())
    if conf.debug:
        stdout_handler.setLevel(logging.DEBUG)
    elif conf.verbose:
        stdout_handler.setLevel(logging.INFO)
    else:
        stdout_handler.setLevel(logging.WARNING)
    log.addHandler(stdout_handler)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    log.addHandler(stderr_handler)