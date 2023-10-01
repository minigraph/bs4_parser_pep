from pathlib import Path

MAIN_DOC_URL = 'https://docs.python.org/3/'
BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
PEP_URL = 'https://peps.python.org/'
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}


class OutputType:
    PRETTY = 'pretty'
    FILE = 'file'


class HTMLTag:
    DIV = 'div'
    A = 'a'
    SECTION = 'section'
    TABLE = 'table'
    H1 = 'h1'
    ABBR = 'abbr'
    DL = 'dl'
    TBODY = 'tbody'
    TR = 'tr'
    UL = 'ul'
    LI = 'li'


class HTMLAttr:
    HREF = 'href'
    CLASS = 'class'
    ID = 'id'


class HTMLValue:
    RFC = 'rfc2822 field-list simple'
    PEP_CONTENT = 'pep-content'
    PEP_ZERO = 'pep-zero-table docutils align-default'
    PEP_REF = 'pep reference internal'
    DOCUTILS = 'docutils'
    SPHINX = 'sphinxsidebarwrapper'
    WHATNEW = 'what-s-new-in-python'
    TREE_WR = 'toctree-wrapper'
    TREE_L1 = 'toctree-l1'
