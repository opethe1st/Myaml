import unittest

from parameterized import parameterized

import myaml


class TestParse(unittest.TestCase):
    @parameterized.expand([
        ('''blah: value''', {'blah': 'value'}
        ),
        ('''key:
    blah: value''', {'key': {'blah': 'value'}}
        ),
        ('''-   -   blah''', [['blah']]
        ),
        ('''
key:
key2:
    ''', {'key': '', 'key2': ''}
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



class TestDump(unittest.TestCase):

    @parameterized.expand([
        ('''blah: value\n''', {'blah': 'value'}
        ),
        ('''key:
    blah: value

''', {'key': {'blah': 'value'}}
        ),
        ('''-   -   blah

''', [['blah']]
        ),
        ('''key: \nkey2: \n''', {'key': '', 'key2': ''}
        ),
        ('''key: value\n''', {'key': 'value'}
        ),
        ('''key: value\nkey2: value2\n''', {'key': 'value', 'key2': 'value2'}
        ),
        ('''key: value
key2:
    key3: value

key4: value
''', {'key': 'value', 'key2': {'key3': 'value'}, 'key4': 'value'}
        ),
        ('''-   key: value

-   key2:
        key3: value


-   value
''', [
                {'key': 'value'},
                {'key2': {'key3': 'value'}},
                'value',
            ]
        ),
    ])
    def test_simple_dumping(self, expected, obj):
        self.assertEqual(myaml.dump(obj=obj), expected)
