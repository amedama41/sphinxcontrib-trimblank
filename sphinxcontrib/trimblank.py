import re
from docutils import nodes

class Trimmer(object):
    CJK_RANGE = (
            r'['
            r'\u2E80-\u9FFF'
            r'\uF900-\uFAFF'    # CJK Compatibility Ideographs
            r'\uFF00-\uFF60\uFFE0-\uFFE6' # Halfwidth and Fullwidth Forms
            r'\U00020000-\U0003FFFF' # Supplementary, Tertiary Ideographic Plane
            r']')
    HEAD_PATTERNS = (
            re.compile(r'^\s\s'),
            re.compile(r'{}$'.format(CJK_RANGE)),
            re.compile(r'^\s{}'.format(CJK_RANGE)))
    TAIL_PATTERNS = (
            re.compile(r'\s\s$'),
            re.compile(r'{}\s$'.format(CJK_RANGE)),
            re.compile(r'^{}'.format(CJK_RANGE)))

    def __init__(self, keep_alnum_blank):
        if keep_alnum_blank:
            pattern = r'(?<={0})[\s](?={0})'
            self._condition = all
        else:
            pattern = r'(?<={0})[\s](?!\s)|(?<!\s)[\s](?={0})'
            self._condition = any
        self._pattern = re.compile(pattern.format(Trimmer.CJK_RANGE))

    def trim_blank(self, target_txt):
        return self._pattern.sub('', target_txt)

    def trim_head(self, target_txt, leading_txt):
        if Trimmer.HEAD_PATTERNS[0].match(target_txt):
            return target_txt
        if not self._check(leading_txt, target_txt, Trimmer.HEAD_PATTERNS):
            return target_txt
        return target_txt.lstrip()

    def trim_tail(self, target_txt, following_txt):
        if Trimmer.TAIL_PATTERNS[0].search(target_txt):
            return target_txt
        if not self._check(target_txt, following_txt, Trimmer.TAIL_PATTERNS):
            return target_txt
        return target_txt.rstrip()

    def _check(self, leading_txt, following_txt, patterns):
        return self._condition((
            patterns[1].search(leading_txt), patterns[2].match(following_txt)))


def trim_text_element(node, trimmer, logger=None):
    target_inline_elems = (nodes.emphasis, nodes.strong)
    num_children = len(node.children)
    for idx, child in enumerate(node.children):
        if not isinstance(child, nodes.Text):
            if isinstance(child, target_inline_elems):
                trim_text_element(child, trimmer, logger)
                pass
            continue
        new_txt = trimmer.trim_blank(child.astext())
        if idx - 1 >= 0:
            prev_txt = node.children[idx - 1].astext()
            new_txt = trimmer.trim_head(new_txt, prev_txt)
        if idx + 1 < num_children:
            next_txt = node.children[idx + 1].astext()
            new_txt = trimmer.trim_tail(new_txt, next_txt)

        if logger is not None and child.astext() != new_txt:
            logger.info(
                    '\nBefore : %s\nAfter  : %s',
                    child.astext(), new_txt, location=child)
        node.replace(child, nodes.Text(new_txt, child.rawsource))


def get_bool_value(config, builder_name):
    if not isinstance(config, (list, tuple)):
        return config
    return builder_name in config

def trimblank(app, doctree, docname):
    builder_name = app.builder.name
    if not get_bool_value(app.config.trimblank_enabled, builder_name):
        return
    keep_alnum_blank = get_bool_value(
            app.config.trimblank_keep_alnum_blank, builder_name)
    trimmer = Trimmer(keep_alnum_blank)
    if app.config.trimblank_debug:
        from sphinx.util import logging
        logger = logging.getLogger(__name__)
    else:
        logger = None

    excluded_elems = (
            nodes.FixedTextElement, nodes.Inline,
            nodes.Invisible, nodes.Bibliographic)
    target_body_elems = lambda n: (
            isinstance(n, nodes.TextElement)
            and not isinstance(n, excluded_elems))
    for node in doctree.traverse(target_body_elems):
        trim_text_element(node, trimmer, logger=logger)


def setup(app):
    types = (bool, list, tuple)
    app.add_config_value('trimblank_enabled', True, 'env', types)
    app.add_config_value('trimblank_keep_alnum_blank', False, 'env', types)
    app.add_config_value('trimblank_debug', False, 'env')
    app.connect("doctree-resolved", trimblank)
