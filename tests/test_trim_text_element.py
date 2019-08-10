import unittest
from unittest.mock import Mock
from docutils import nodes
from sphinxcontrib.trimblank import trim_text_element

class TrimTextElementTest(unittest.TestCase):
    def setUp(self):
        self.trimmer = Mock()
        self.trimmer.trim_blank.side_effect = lambda txt: 'blank(%s)' % txt
        self.trimmer.trim_head.side_effect = lambda txt, p: 'head(%s)' % txt
        self.trimmer.trim_tail.side_effect = lambda txt, n: 'tail(%s)' % txt
        self.text_elem = nodes.TextElement(rawsource='', text='')

    def test_without_text(self):
        elems = []
        self.text_elem.extend(elems)

        trim_text_element(self.text_elem, self.trimmer)

        self.assertEqual(self.text_elem.astext(), '')
        self.trimmer.trim_blank.assert_not_called()
        self.trimmer.trim_head.assert_not_called()
        self.trimmer.trim_tail.assert_not_called()

    def test_with_single_text(self):
        elems = [nodes.Text('あなたは私を食べる')]
        self.text_elem.extend(elems)

        trim_text_element(self.text_elem, self.trimmer)

        self.assertEqual(self.text_elem.astext(), 'blank(あなたは私を食べる)')
        self.trimmer.trim_head.assert_not_called()
        self.trimmer.trim_tail.assert_not_called()

    def test_with_multiple_text(self):
        elems = [nodes.Text('あなたは'), nodes.Text('私を食べる')]
        self.text_elem.extend(elems)

        trim_text_element(self.text_elem, self.trimmer)

        self.assertEqual(
                self.text_elem.astext(),
                'tail(blank(あなたは))head(blank(私を食べる))')

    def test_with_single_inline_element(self):
        elems = [nodes.strong(text='あなたは私を食べる')]
        self.text_elem.extend(elems)

        trim_text_element(self.text_elem, self.trimmer)

        self.assertEqual(self.text_elem.astext(), 'blank(あなたは私を食べる)')
        self.trimmer.trim_head.assert_not_called()
        self.trimmer.trim_tail.assert_not_called()

    def test_with_multiple_inline_element(self):
        elems = [
                nodes.strong(text='あなたは'),
                nodes.emphasis(text='私を食べる')
        ]
        self.text_elem.extend(elems)

        trim_text_element(self.text_elem, self.trimmer)

        self.assertEqual(
                self.text_elem.astext(),
                'blank(あなたは)blank(私を食べる)')
        self.trimmer.trim_head.assert_not_called()
        self.trimmer.trim_tail.assert_not_called()

    def test_with_multiple_nested_inline_element(self):
        elems = [
                nodes.strong(
                    '', '',
                    nodes.Text('あなたは'), nodes.emphasis(text='私を食べる'))
        ]
        self.text_elem.extend(elems)

        trim_text_element(self.text_elem, self.trimmer)

        self.assertEqual(
                self.text_elem.astext(),
                'tail(blank(あなたは))blank(私を食べる)')

