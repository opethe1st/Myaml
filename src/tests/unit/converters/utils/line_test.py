import unittest

from parameterized import parameterized

from myaml.converters.utils.line import (
    Line,
    get_indent,
    get_lines,
    get_string,
    get_string_from_lines,
    line_from_string,
)


class TestGetLines(unittest.TestCase):

    def test_get_lines(self):
        string = '''
key:
    key: value
    key: value
key: value'''
        expectedLines = [
            Line(indent=0, string='key:'),
            Line(indent=1, string='key: value'),
            Line(indent=1, string='key: value'),
            Line(indent=0, string='key: value'),
        ]
        self.assertEqual(get_lines(string=string), expectedLines)


class TestGetStringFromLines(unittest.TestCase):

    def test_get_string_from_lines(self):
        lines = [
            Line(indent=0, string='key:'),
            Line(indent=1, string='key: value'),
            Line(indent=1, string='key: value'),
            Line(indent=0, string='key: value'),
        ]
        expectedString = '''key:
    key: value
    key: value
key: value'''
        self.assertEqual(get_string_from_lines(lines=lines), expectedString)


class TestFromString(unittest.TestCase):

    @parameterized.expand([
        ('the indent', Line(indent=0, string='the indent')),
        ('    the value', Line(indent=1, string='the value')),
        ('        the value', Line(indent=2, string='the value')),
        ('        key: value', Line(indent=2, string='key: value')),
        ('        key: value  ', Line(indent=2, string='key: value  ')),
    ])
    def test_from_string(self, string, expectedLine):
        self.assertEqual(line_from_string(string=string), expectedLine)


class TestGetIndent(unittest.TestCase):

    @parameterized.expand([
        ('the indent', 0),
        ('    the value', 1),
        ('        the value', 2),
    ])
    def test_get_indent(self, string, expectedIndent):
        self.assertEqual(first=get_indent(string=string), second=expectedIndent)


class TestGetString(unittest.TestCase):

    @parameterized.expand([
        ('the indent', 'the indent'),
        ('    the value', 'the value'),
        ('        the value', 'the value'),
        ('        key: value', 'key: value'),
        ('        key: value  ', 'key: value  '),
    ])
    def test_get_indent(self, string, expectedIndent):
        self.assertEqual(first=get_string(string=string), second=expectedIndent)
