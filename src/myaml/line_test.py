import unittest

from parameterized import parameterized

from .line import Line


class LineTestCase(unittest.TestCase):
    pass


class TestgetLines(LineTestCase):

    def test_get_lines(self):
        string = '''
key:
    key: value
    key: value
key: value'''
        expectedLines = [
            Line(indent=0, string=''),
            Line(indent=0, string='key:'),
            Line(indent=1, string='key: value'),
            Line(indent=1, string='key: value'),
            Line(indent=0, string='key: value'),
        ]
        self.assertEqual(Line._get_lines(string=string), expectedLines)


class TestgetStringFromLines(LineTestCase):

    def test_get_string_from_lines(self):
        lines = [
            Line(indent=0, string=''),
            Line(indent=0, string='key:'),
            Line(indent=1, string='key: value'),
            Line(indent=1, string='key: value'),
            Line(indent=0, string='key: value'),
        ]
        expectedString = '''
key:
    key: value
    key: value
key: value'''
        self.assertEqual(Line._get_string_from_lines(lines=lines), expectedString)


class TestFromString(LineTestCase):

    @parameterized.expand([
        ('the indent', Line(indent=0, string='the indent')),
        ('    the value', Line(indent=1, string='the value')),
        ('        the value', Line(indent=2, string='the value')),
        ('        key: value', Line(indent=2, string='key: value')),
        ('        key: value  ', Line(indent=2, string='key: value  ')),
    ])
    def test_from_string(self, string, expectedLine):
        self.assertEqual(Line.from_string(string=string), expectedLine)


class TestgetIndent(LineTestCase):

    @parameterized.expand([
        ('the indent', 0),
        ('    the value', 1),
        ('        the value', 2),
    ])
    def test_get_indent(self, string, expectedIndent):
        self.assertEqual(first=Line._get_indent(string=string), second=expectedIndent)


class TestgetString(LineTestCase):

    @parameterized.expand([
        ('the indent', 'the indent'),
        ('    the value', 'the value'),
        ('        the value', 'the value'),
        ('        key: value', 'key: value'),
        ('        key: value  ', 'key: value  '),
    ])
    def test_get_indent(self, string, expectedIndent):
        self.assertEqual(first=Line._get_string(string=string), second=expectedIndent)
