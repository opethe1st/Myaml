import unittest

from parameterized import parameterized

from ._utils import get_key_value_strings
from ._utils import get_element_strings


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
