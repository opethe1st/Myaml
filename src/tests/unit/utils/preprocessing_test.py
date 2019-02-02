import unittest

from parameterized import parameterized

from myaml.utils import (
    format_to_canonical_form,
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
            format_to_canonical_form(string=string),
            expected
        )
