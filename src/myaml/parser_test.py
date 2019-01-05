import unittest

import pytest

from .parser import Parser
from .exceptions import ParsingException


class ParserTestCase(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()


class TestGetIndentLevel(ParserTestCase):

    def test_get_indent_level_works_when_space_is_multiple_of_indent(self):
        indent_level = self.parser._get_indent_level(line='  b')
        expected_indent_level = 1
        self.assertEqual(indent_level, expected_indent_level)

    def test_get_indent_level_raises_exception_when_space_not_multiple_of_indent(self):
        with pytest.raises(ParsingException):
            self.parser._get_indent_level(line=' blah')


class TestGetKey(ParserTestCase):

    def test_get_key_works_if_line_matches_the_expected_pattern_and_no_space_at_the_end(self):
        key = self.parser._get_key(line='key:')
        expectedKey = 'key'
        self.assertEqual(key, expectedKey)

    def test_get_key_works_if_line_matches_the_expected_pattern_and_one_space_at_the_end(self):
        key = self.parser._get_key(line='key: ')
        expectedKey = 'key'
        self.assertEqual(key, expectedKey)

    def test_get_key_works_if_line_matches_the_expected_pattern_and_multiple_spaces_at_the_end(self):
        key = self.parser._get_key(line='key:       ')
        expectedKey = 'key'
        self.assertEqual(key, expectedKey)

    def test_get_key_raises_exception_if_lines_doesnt_match_expected_pattern(self):
        with pytest.raises(ParsingException):
            self.parser._get_key(line='key')
