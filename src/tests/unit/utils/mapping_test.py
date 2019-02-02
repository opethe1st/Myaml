import unittest

from parameterized import parameterized

from myaml.utils import (
    get_key_value_strings,
)


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
