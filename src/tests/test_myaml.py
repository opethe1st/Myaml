import unittest

from parameterized import parameterized

import myaml


class TestParse(unittest.TestCase):
    @parameterized.expand([
        ('''
key:
    blah:
    ''', {'key': {'blah': {}}}
        ),
        ('''
key:
    blah:
key2:
    ''', {'key': {'blah': {}}, 'key2': {}}
        ),
        ('''
key:
key2:
    ''', {'key': {}, 'key2': {}}
        ),
        ('''
key: value
    ''', {'key': 'value'}
        ),
        ('''
key: value
key2: value2
    ''', {'key': 'value', 'key2': 'value2'}
        ),
            ('''
key: value
key2: value2
    ''', {'key': 'value', 'key2': 'value2'}
        ),
        ('''
key: value
key2:
    key3: value
key4: value
    ''', {'key': 'value', 'key2': {'key3': 'value'}, 'key4': 'value'}
        ),
        ('''
- key: value
- key2:
    key3: value
- value
    ''', [
                {'key': 'value'},
                {'key2': {'key3': 'value'}},
                'value',
            ]
        ),
    ])
    def test_simple_parsing(self, string, expected):
        self.assertEqual(myaml.parse(string=string), expected)
