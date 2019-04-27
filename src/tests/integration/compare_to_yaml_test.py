import unittest

import yaml
from parameterized import parameterized

import myaml


class TestYamlLoad(unittest.TestCase):
    @parameterized.expand([
        ('''blah: value''',
        ),
        ('''key:
    blah: value''',
        ),
        ('''-   -   blah''',),
        ('''
key:
key2:''',
        ),
        ('''
key: value''',
        ),
        ('''
key: value
key2: value2''',
        ),
        ('''
key: value
key2: value2''',
        ),
        ('''
key: value
key2:
    key3: value
key4: value''',
        ),
        ('''
- key: value
- key2:
    key3: value
- value''',
        ),
        ('''
key:
  key: value''',
        ),
        ('''
# blah blah blah
    # blah
key:
  key: value''',
        ),
        ('''
key:
  - key: value''',
        ),
        ('''
key:
  - key: value#1232''',
        ),
        ('''
value-1232''',
        ),
        ('''
value:1232''',
        ),
    ])
    def test_loading(self, string):
        self.assertEqual(
            myaml.load(string=string),
            yaml.load(string, Loader=yaml.SafeLoader)
        )
