import unittest
import yaml
from parameterized import parameterized

import myaml


class TestLoad(unittest.TestCase):
    @parameterized.expand([
        (
            'test that a simple mapping works',
            '''blah: value''',
            {'blah': 'value'}
        ),
        (
            'test that a nested mapping works',
            '''key:
    blah: value''',
            {'key': {'blah': 'value'}}
        ),
        (
            'test that a sequence in a sequence works',
            '''-   -   blah''',
            [['blah']]
        ),
        (
            'test that it works when the value of a mapping is empty',
            '''
key:
key2:''',
            {'key': None, 'key2': None}
        ),
        (
            'test that a simple mapping works when there is a newline at the beginning',
            '''
key: value''',
            {'key': 'value'}
        ),
        (
            'test that it works when the key are mapping have spaces in them',
            '''
this is a key: this is a value''',
            {'this is a key': 'this is a value'}
        ),
        (
            'test that it works when the key and nested mapping have spaces in them',
            '''
this is a key:
    this is another key: this is a value
        ''',
            {
                'this is a key':
                {'this is another key': 'this is a value'}
            }
        ),
        (
            'test that mappings with more than one item works',
            '''
key: value
key2: value2''',
            {'key': 'value', 'key2': 'value2'}
        ),
        (
            'test that nested mappings works with more than one item works',
            '''
key: value
key2:
    key3: value
key4: value''',
            {'key': 'value', 'key2': {'key3': 'value'}, 'key4': 'value'}
        ),
        (
            'test that sequences with nested item works',
            '''
- key: value
- key2:
    key3: value
- value''',
            [
                {'key': 'value'},
                {'key2': {'key3': 'value'}},
                'value',
            ]
        ),
        (
            'test that nest mapping works when the indent is 2 spaces wide',
            '''
key:
  key: value
   ''',
            {'key': {'key': 'value'}}
        ),
        (
            'test that it works when there are comments',
            '''
# blah blah blah
    # blah
key:
  key: value''',
            {'key': {'key': 'value'}}
        ),
        (
            'test that it works when an item in the sequence is a mapping',
            '''
key:
  - key: value''',
            {'key': [{'key': 'value'}]}
        ),
        (
            'test that values with # work',
            '''
key:
  - key: value#1232''',
            {'key': [{'key': 'value#1232'}]}
        ),
        (
            'test that values with "-" work',
            '''
value-1232''',
            'value-1232'
        ),
        (
            'test that values with ":" work',
            '''
value:1232
 ''',
            'value:1232'
        ),
    ])
    def test_loading(self, name, string, expected):
        self.assertEqual(myaml.load(string=string), expected)
        self.assertEqual(myaml.load(string=string), yaml.load(string, Loader=yaml.SafeLoader))

    @parameterized.expand([
        (
            'test that exception is raised if there is inconsistent indentation',
            '''
key:
  key: value
     key: value''',
            myaml.exceptions.TokenizationException,
            'This error: "Inconsistent Indentation" occurred at line 4, column 6'
        ),
        (
            'test that an exception is raised when there is weird indentation',
            '''
    key: value
    key: value
key:
''',
            myaml.exceptions.ParsingException,
            'Unexpected indent level. What is you doing!'
        ),
        (
            'test that an exception is raised if we expect a sequence item but get something else',
            '''
- key: value
- key: value
key:
''',
            myaml.exceptions.ParsingException,
            'Unexpected indent level. What is you doing!'
        ),
    ])
    def test_raise_exception(self, name, string, expectedException, message):
        with self.assertRaises(expectedException) as exceptionContext:
            myaml.load(string=string)
        self.assertEqual(str(exceptionContext.exception), message)


class TestDump(unittest.TestCase):

    @parameterized.expand([
        (
            'test that simple mappings work',
            '''blah: value\n''',
            {'blah': 'value'}
        ),
        (
            'test that nested mappings work',
            '''key:
    blah: value
''',
            {'key': {'blah': 'value'}}
        ),
        (
            'test that a sequence in a sequence is dumped properly',
            '''-   -   blah
''',
            [['blah']]
        ),
        (
            'test that a mapping that has empty values is dumped properly',
            '''key: \nkey2: \n''',
            {'key': '', 'key2': ''}
        ),
        (
            'test that a mapping with more than one item is dumped properly',
            '''key: value\nkey2: value2\n''',
            {'key': 'value', 'key2': 'value2'}
        ),
        (
            'test that a mapping with nested items is dumped properly',
            '''key: value
key2:
    key3: value
key4: value
''',
            {'key': 'value', 'key2': {'key3': 'value'}, 'key4': 'value'}
        ),
        (
            'test that sequence with scalar and mapping items is dumped properly',
            '''-   key: value
-   key2:
        key3: value
-   value
''',
            [
                {'key': 'value'},
                {'key2': {'key3': 'value'}},
                'value',
            ]
        ),
    ])
    def test_dumping(self, name, expected, obj):
        self.assertEqual(myaml.dump(obj=obj), expected)
