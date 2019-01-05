import pytest

import myaml


@pytest.mark.parametrize(
    "string,expected",
    [
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
    ]
)
def test_simple_parsing(string, expected):
    assert myaml.parse(string=string) == expected
