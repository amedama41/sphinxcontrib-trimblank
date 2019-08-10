import unittest
from sphinxcontrib.trimblank import Trimmer

class TrimmerWithoutKeepBlankTest(unittest.TestCase):
    def setUp(self):
        self.sut = Trimmer(False)

    def test_trim_blank(self):
        datalist = [
                ('あなたは 私を 食べる', 'あなたは私を食べる'),
                ('You は me を食べる', 'Youはmeを食べる'),
                ('You eat me', 'You eat me'),
                ('あなたは\n私を\n食べる', 'あなたは私を食べる'),
                ('You\nは\nme\nを食べる', 'Youはmeを食べる'),
                ('You\neat\nme', 'You\neat\nme'),
                ('あなたは  私を  食べる', 'あなたは  私を  食べる'),
                ('You  は  me  を食べる', 'You  は  me  を食べる'),
                ('You  eat  me', 'You  eat  me'),
                (' ', ' '),
                ('', ''),
        ]
        for txt, expected in datalist:
            with self.subTest(txt=txt, expected=expected):
                result = self.sut.trim_blank(txt)

                self.assertEqual(result, expected)

    def test_trim_head(self):
        datalist = [
                ('あなたは', ' 私を食べる', '私を食べる'),
                ('You', ' は me を食べる', 'は me を食べる'),
                ('You', ' eat me', ' eat me'),
                ('あなたは', '\n私を食べる', '私を食べる'),
                ('You', '\nは me を食べる', 'は me を食べる'),
                ('You', '\neat me', '\neat me'),
                ('あなたは', '  私を食べる', '  私を食べる'),
                ('You', '  は me を食べる', '  は me を食べる'),
                ('You', '  eat me', '  eat me'),
                ('あなたは', ' ', ''),
                ('You', ' ', ' '),
                ('You', ' ', ' '),
                ('あなたは', '', ''),
                ('You', '', ''),
                ('You', '', ''),
        ]
        for prev_txt, txt, expected in datalist:
            with self.subTest(prev_txt=prev_txt, txt=txt, expected=expected):
                result = self.sut.trim_head(txt, prev_txt)

                self.assertEqual(result, expected)

    def test_trim_tail(self):
        datalist = [
                ('あなたは私を ', '食べる', 'あなたは私を'),
                ('You は ', 'me を食べる', 'You は'),
                ('You eat ', 'me', 'You eat '),
                ('あなたは私を\n', '食べる', 'あなたは私を'),
                ('You は\n', 'me を食べる', 'You は'),
                ('You eat\n', 'me', 'You eat\n'),
                ('あなたは私を  ', '食べる', 'あなたは私を  '),
                ('You は  ', 'me を食べる', 'You は  '),
                ('You eat  ', 'me', 'You eat  '),
                (' ', '食べる', ''),
                (' ', 'me を食べる', ' '),
                (' ', 'me', ' '),
                ('', '食べる', ''),
                ('', 'me を食べる', ''),
                ('', 'me', ''),
        ]
        for txt, next_txt, expected in datalist:
            with self.subTest(txt=txt, next_txt=next_txt, expected=expected):
                result = self.sut.trim_tail(txt, next_txt)

                self.assertEqual(result, expected)

class TrimmerWithKeepBlankTest(unittest.TestCase):
    def setUp(self):
        self.sut = Trimmer(True)

    def test_trim_blank(self):
        datalist = [
                ('あなたは 私を 食べる', 'あなたは私を食べる'),
                ('You は me を食べる', 'You は me を食べる'),
                ('You eat me', 'You eat me'),
                ('あなたは\n私を\n食べる', 'あなたは私を食べる'),
                ('You\nは\nme\nを食べる', 'You\nは\nme\nを食べる'),
                ('You\neat\nme', 'You\neat\nme'),
                ('あなたは  私を  食べる', 'あなたは  私を  食べる'),
                ('You  は  me  を食べる', 'You  は  me  を食べる'),
                ('You  eat  me', 'You  eat  me'),
                (' ', ' '),
                ('', ''),
        ]
        for txt, expected in datalist:
            with self.subTest(txt=txt, expected=expected):
                result = self.sut.trim_blank(txt)

                self.assertEqual(result, expected)

    def test_trim_head(self):
        datalist = [
                ('あなたは', ' 私を食べる', '私を食べる'),
                ('You', ' は me を食べる', ' は me を食べる'),
                ('You', ' eat me', ' eat me'),
                ('あなたは', '\n私を食べる', '私を食べる'),
                ('You', '\nは me を食べる', '\nは me を食べる'),
                ('You', '\neat me', '\neat me'),
                ('あなたは', '  私を食べる', '  私を食べる'),
                ('You', '  は me を食べる', '  は me を食べる'),
                ('You', '  eat me', '  eat me'),
                ('あなたは', ' ', ' '),
                ('You', ' ', ' '),
                ('You', ' ', ' '),
                ('あなたは', '', ''),
                ('You', '', ''),
                ('You', '', ''),
        ]
        for prev_txt, txt, expected in datalist:
            with self.subTest(prev_txt=prev_txt, txt=txt, expected=expected):
                result = self.sut.trim_head(txt, prev_txt)

                self.assertEqual(result, expected)

    def test_trim_tail(self):
        datalist = [
                ('あなたは私を ', '食べる', 'あなたは私を'),
                ('You は ', 'meを食べる', 'You は '),
                ('You eat ', 'me', 'You eat '),
                ('あなたは私を\n', '食べる', 'あなたは私を'),
                ('You は\n', 'meを食べる', 'You は\n'),
                ('You eat\n', 'me', 'You eat\n'),
                ('あなたは私を  ', '食べる', 'あなたは私を  '),
                ('You は  ', 'meを食べる', 'You は  '),
                ('You eat  ', 'me', 'You eat  '),
                (' ', '食べる', ' '),
                (' ', 'me を食べる', ' '),
                (' ', 'me', ' '),
                ('', '食べる', ''),
                ('', 'me を食べる', ''),
                ('', 'me', ''),
        ]
        for txt, next_txt, expected in datalist:
            with self.subTest(txt=txt, next_txt=next_txt, expected=expected):
                result = self.sut.trim_tail(txt, next_txt)

                self.assertEqual(result, expected)
