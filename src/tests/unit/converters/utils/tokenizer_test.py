import unittest

from parameterized import parameterized

from myaml.converters.utils import tokenize
from myaml.converters.utils.tokenizer import (
    Indent,
    Newline,
    Separator,
    SequenceIndent,
    Value
)


class TestTokenizer(unittest.TestCase):

    # there are possibly too many test cases here. plus I wish I could use a @test decorator instead of name mangling.
    @parameterized.expand([
        ('', []),
        ('''a
''', [Value(data='a'), Newline()]),
        ('key: value', [Value(data='key'), Separator(), Value(data='value')]),
        ('key', [Value(data='key')]),
        ('key:value', [Value(data='key:value')]),
        ('key:123: value', [Value(data='key:123'), Separator(), Value(data='value')]),
        ('key-123: value', [Value(data='key-123'), Separator(), Value(data='value')]),
        ('-key123: value', [Value(data='-key123'), Separator(), Value(data='value')]),
        ('  key', [Indent(), Value(data='key')]),
        ('''key:
  value''',
        [Value(data='key'), Separator(), Newline(), Indent(), Value(data='value')]
        ),
        ('''key:
  key: value''',
            [
                Value(data='key'),
                Separator(),
                Newline(),
                Indent(),
                Value(data='key'),
                Separator(),
                Value(data='value'),
            ]
        ),
        ('''key:
  key:
    key1: value''',
            [
                Value(data='key'),
                Separator(),
                Newline(),
                Indent(),
                Value(data='key'),
                Separator(),
                Newline(),
                Indent(),
                Indent(),
                Value(data='key1'),
                Separator(),
                Value(data='value'),
            ]
        ),
        ('''key:
- key: value''',
            [
                Value(data='key'),
                Separator(),
                Newline(),
                SequenceIndent(),
                Value(data='key'),
                Separator(),
                Value(data='value'),
            ]
        ),
        ('''key:
  - key: value''',
            [
                Value(data='key'),
                Separator(),
                Newline(),
                Indent(),
                SequenceIndent(),
                Value(data='key'),
                Separator(),
                Value(data='value'),
            ]
        ),
        (' ', []),
        ('#abc', []),
        (' #abc', []),
        ('# abc', []),
        ('key: #abc', [Value(data='key'), Separator()]),
        ('key:#abc', [Value(data='key:#abc')]),
        ('''key:
  key1: value #abc''',
            [
                Value(data='key'),
                Separator(),
                Newline(),
                Indent(),
                Value(data='key1'),
                Separator(),
                Value(data='value'),
            ]
        ),
        (' # abc', []),
        ('''# abc
''', []),
        ('''# abc
key: value''', [Value(data='key'), Separator(), Value(data='value')]
        ),
        (
            '''key: value # abc''', [Value(data='key'), Separator(), Value(data='value')]
        ),
        (
            '''key: value # abc''', [Value(data='key'), Separator(), Value(data='value')]
        ),
        (
            '''key: value#abc''', [Value(data='key'), Separator(), Value(data='value#abc')]
        ),
        (
            '''#key
key: value#abc''', [Value(data='key'), Separator(), Value(data='value#abc')]
        ),
    ])
    def test_key_value(self, string, expectedTokens):
        self.assertEqual(
            tokenize(string=string),
            expectedTokens,
        )

    @parameterized.expand([
        (' key', Exception),
        ('-  key', Exception)  # because there are two spaces.
    ])
    def test_key_value(self, string, expectedException):
        with self.assertRaises(expected_exception=expectedException):
            tokenize(string=string)
