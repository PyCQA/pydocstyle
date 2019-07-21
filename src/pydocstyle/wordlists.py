"""Wordlists loaded from package data.

We can treat them as part of the code for the imperative mood check, and
therefore we load them at import time, rather than on-demand.

"""
import re
import pkgutil
import snowballstemmer
from collections import defaultdict
from typing import Iterator, List, Dict


#: Regular expression for stripping comments from the wordlists
COMMENT_RE = re.compile(r'\s*#.*')

#: Stemmer function for stemming words in English
stem = snowballstemmer.stemmer('english').stemWord


def load_wordlist(name: str) -> Iterator[str]:
    """Iterate over lines of a wordlist data file.

    `name` should be the name of a package data file within the data/
    directory.

    Whitespace and #-prefixed comments are stripped from each line.

    """
    data = pkgutil.get_data('pydocstyle', 'data/' + name)
    if data is not None:
        text = data.decode('utf8')
        for line in text.splitlines():
            line = COMMENT_RE.sub('', line).strip()
            if line:
                yield line


#: A dict mapping stemmed verbs to the imperative form
IMPERATIVE_VERBS = defaultdict(list)  # type: Dict[str, List[str]]
for verb in load_wordlist('imperatives.txt'):
    IMPERATIVE_VERBS[stem(verb)].append(verb)

#: Words that are forbidden to appear as the first word in a docstring
IMPERATIVE_BLACKLIST = set(load_wordlist('imperatives_blacklist.txt'))
