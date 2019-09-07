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
    # Blanks after this pattern are always kept.
    HEAD_PATTERNS = (
        re.compile(r'{}$'.format(CJK_RANGE)),
        re.compile(r'^\s{}'.format(CJK_RANGE)))
    TAIL_PATTERNS = (
        re.compile(r'{}\s$'.format(CJK_RANGE)),
        re.compile(r'^{}'.format(CJK_RANGE)))

    def __init__(self, keep_alnum_blank, keep_blank_before, keep_blank_after):
        if keep_alnum_blank:
            pattern = r'(?<={0})\s(?={0})'
            self._condition = all
        else:
            pattern = (r'(?<={0})\s(?!%s)|(?<!%s)\s(?={0})'
                       % (keep_blank_before, keep_blank_after))
            self._condition = any
        self._pattern = re.compile(pattern.format(Trimmer.CJK_RANGE))
        self._head_exlusion_pattern = re.compile(r'^\s%s' % keep_blank_before)
        self._tail_exlusion_pattern = re.compile(r'%s\s$' % keep_blank_after)

    def trim_blank(self, target_txt):
        return self._pattern.sub('', target_txt)

    def trim_head(self, target_txt, leading_txt):
        if self._head_exlusion_pattern.match(target_txt):
            return target_txt
        if not self._check(leading_txt, target_txt, Trimmer.HEAD_PATTERNS):
            return target_txt
        return target_txt.lstrip()

    def trim_tail(self, target_txt, following_txt):
        if self._tail_exlusion_pattern.search(target_txt):
            return target_txt
        if not self._check(target_txt, following_txt, Trimmer.TAIL_PATTERNS):
            return target_txt
        return target_txt.rstrip()

    def _check(self, leading_txt, following_txt, patterns):
        return self._condition((
            patterns[0].search(leading_txt), patterns[1].match(following_txt)))


class TrimblankVisitor(nodes.GenericNodeVisitor):
    EXCLUDED_ELEMENTS = (
        nodes.FixedTextElement, nodes.Inline,
        nodes.Invisible, nodes.Bibliographic)

    def __init__(self, document, trimmer, logger=None):
        super(TrimblankVisitor, self).__init__(document)
        self._trimmer = trimmer
        self._logger = logger

    def default_visit(self, node):
        if not isinstance(node, nodes.TextElement):
            return
        if isinstance(node, TrimblankVisitor.EXCLUDED_ELEMENTS):
            return
        self._trim_blank(node)
        raise nodes.SkipChildren

    def default_departure(self, _node):
        assert False, 'Never use depature method'

    def unknown_visit(self, node):
        self.default_visit(node)

    def _trim_blank(self, node):
        target_inline_elems = (nodes.emphasis, nodes.strong)
        num_children = len(node.children)
        for idx, child in enumerate(node.children):
            if not isinstance(child, nodes.Text):
                if isinstance(child, target_inline_elems):
                    self._trim_blank(child)
                continue
            new_txt = self._trimmer.trim_blank(child.astext())
            if idx - 1 >= 0:
                prev_txt = node.children[idx - 1].astext()
                new_txt = self._trimmer.trim_head(new_txt, prev_txt)
            if idx + 1 < num_children:
                next_txt = node.children[idx + 1].astext()
                new_txt = self._trimmer.trim_tail(new_txt, next_txt)

            if self._logger is not None and child.astext() != new_txt:
                self._logger.info(
                    '\nBefore : %s\nAfter  : %s',
                    child.astext(), new_txt, location=child)
            node.replace(child, nodes.Text(new_txt, child.rawsource))


def get_bool_value(config, builder_name):
    if not isinstance(config, (list, tuple)):
        return config
    return builder_name in config

def trimblank(app, doctree, _docname):
    builder_name = app.builder.name
    if not get_bool_value(app.config.trimblank_enabled, builder_name):
        return
    keep_alnum_blank = get_bool_value(
        app.config.trimblank_keep_alnum_blank, builder_name)
    trimmer = Trimmer(keep_alnum_blank,
                      app.config.trimblank_keep_blank_before,
                      app.config.trimblank_keep_blank_after)
    if app.config.trimblank_debug:
        from sphinx.util import logging
        logger = logging.getLogger(__name__)
    else:
        logger = None

    visitor = TrimblankVisitor(doctree, trimmer, logger)
    doctree.walk(visitor)


def setup(app):
    types = (bool, list, tuple)
    app.add_config_value('trimblank_enabled', True, 'env', types)
    app.add_config_value('trimblank_keep_alnum_blank', False, 'env', types)
    app.add_config_value('trimblank_keep_blank_before', r'[\s(]', 'env', str)
    app.add_config_value('trimblank_keep_blank_after', r'[\s),.:?]', 'env', str)
    app.add_config_value('trimblank_debug', False, 'env')
    app.connect("doctree-resolved", trimblank)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
