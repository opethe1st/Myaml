import unittest

from parameterized import parameterized

from myaml._utils import get_key_value_strings
from myaml._utils import get_element_strings
from myaml._utils import convert_to_string_with_desired_indent


class TestGetKeyValueStrings(unittest.TestCase):
    @parameterized.expand([
        ('key: value', ['key: value']),
        ('''key: value
key3: value
key2: value''', ['key: value', 'key3: value', 'key2: value']),
        ('', [])
    ])
    def test_get_key_value_strings(self, string, expected):
        self.assertEqual(
            get_key_value_strings(string=string),
            expected
        )


class TestElementStrings(unittest.TestCase):
    @parameterized.expand([
        ('-   key: value', ['    key: value']),
        ('''-   key: value
-   key3: value
-   key2: value''', ['    key: value', '    key3: value', '    key2: value']),
        ('', [])
    ])
    def test_get_key_value_strings(self, string, expected):
        self.assertEqual(
            get_element_strings(string=string),
            expected
        )


class TestConvertToStringWithDesiredIndent(unittest.TestCase):
    @parameterized.expand([
        ('''key:
     key: value''',
'''key:
    key: value'''
        )
    ])
    def test_convert_to_string_with_desired_indent(self, string, expected):
        self.assertEqual(
            convert_to_string_with_desired_indent(string=string),
            expected
        )
