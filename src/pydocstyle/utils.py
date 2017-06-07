"""General shared utilities."""
import logging
from itertools import tee
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

from docutils import utils
from docutils.core import Publisher
from docutils.nodes import Element

# Do not update the version manually - it is managed by `bumpversion`.
__version__ = '2.0.1rc'
log = logging.getLogger(__name__)


def is_blank(string):
    """Return True iff the string contains only whitespaces."""
    return not string.strip()


def pairwise(iterable, default_value):
    """Return pairs of items from `iterable`.

    pairwise([1, 2, 3], default_value=None) -> (1, 2) (2, 3), (3, None)
    """
    a, b = tee(iterable)
    _ = next(b, default_value)
    return zip_longest(a, b, fillvalue=default_value)

def rst_lint(docstring_content):
    """Lint reStructuredText and return errors

    :param string content: reStructuredText to be linted
    :rtype list: List of errors. Each error will contain a line, message (error
        message), and full message (error message + source lines)

    Based on public domain code by Todd Wolfson in his tool restructuredtext-lint
    https://github.com/twolfson/restructuredtext-lint/blob/master/restructuredtext_lint/lint.py
    """
    # Generate a new parser (copying `rst2html.py` flow)
    pub = Publisher(None, None, None, settings=None)
    pub.set_components('standalone', 'restructuredtext', 'pseudoxml')

    # Configure publisher
    # DEV: We cannot use `process_command_line` since it processes `sys.argv`
    settings = pub.get_settings(halt_level=5)
    pub.set_io()

    # Prepare a document to parse on
    # DEV: We avoid the `read` method because when `source` is `None`,
    #      it attempts to read from `stdin`.
    #      However, we already know our content.
    # DEV: We create our document without `parse` because we need to
    #      attach observer's before parsing
    reader = pub.reader
    document = utils.new_document(None, settings)

    # Disable stdout
    document.reporter.stream = None

    # Collect errors via an observer
    errors = []

    def error_collector(data):
        errors.append(Element.astext(data.children[0]).replace("\n", " "))

    document.reporter.attach_observer(error_collector)

    # Parse the content (and collect errors)
    reader.parser.parse(docstring_content, document)
    # Apply transforms (and more collect errors)
    # DEV: We cannot use `apply_transforms` since it has
    # `attach_observer` baked in. We want only our listener.
    document.transformer.populate_from_components(
        (pub.source, pub.reader, pub.reader.parser, pub.writer, pub.destination)
    )
    transformer = document.transformer
    while transformer.transforms:
        if not transformer.sorted:
            # Unsorted initially, and whenever a transform is added.
            transformer.transforms.sort()
            transformer.transforms.reverse()
            transformer.sorted = 1
        priority, transform_class, pending, kwargs = transformer.transforms.pop()
        transform = transform_class(transformer.document, startnode=pending)
        transform.apply(**kwargs)
        transformer.applied.append((priority, transform_class, pending, kwargs))
    return errors
