import unittest

from parameterized import parameterized

from myaml.loading.tokenizer import (
    Indent,
    Newline,
    Separator,
    SequenceIndent,
    Value,
    tokenize
)


class TestTokenizer(unittest.TestCase):

    # there are possibly too many test cases here. plus I wish I could use a @test decorator instead of name mangling.
    @parameterized.expand([
        ('', []),
        ('''a
''', [Value(data='a'), Newline()]),
        ('key: value', [Value(data='key'), Separator(), Value(data='value'), Newline()]),
        ('key', [Value(data='key'), Newline()]),
        ('key:value', [Value(data='key:value'), Newline()]), # they all have Newlines at the end, figure out a fix later if necessary
        ('key:123: value', [Value(data='key:123'), Separator(), Value(data='value'), Newline()]),
        ('key-123: value', [Value(data='key-123'), Separator(), Value(data='value'), Newline()]),
        ('-key123: value', [Value(data='-key123'), Separator(), Value(data='value'), Newline()]),
        ('  key', [Indent(), Value(data='key'), Newline()]),
        ('''key:
  value''',
        [Value(data='key'), Separator(), Newline(), Indent(), Value(data='value'), Newline()]
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
                Newline(),
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
                Newline(),
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
                Newline(),
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
                Newline(),
            ]
        ),
        (' ', []),
        ('#abc', []),
        (' #abc', []),
        ('# abc', []),
        ('key: #abc', [Value(data='key'), Separator()]),
        ('key:#abc', [Value(data='key:#abc'), Newline()]),
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
key: value''', [Value(data='key'), Separator(), Value(data='value'), Newline()]
        ),
        (
            '''key: value # abc''', [Value(data='key'), Separator(), Value(data='value')]
        ),
        (
            '''key: value # abc''', [Value(data='key'), Separator(), Value(data='value')]
        ),
        (
            '''key: value#abc''', [Value(data='key'), Separator(), Value(data='value#abc'), Newline()]
        ),
        (
            '''#key
key: value#abc''', [Value(data='key'), Separator(), Value(data='value#abc'), Newline()]
        ),
        (
            '''
   key: value#abcd''', [Indent(), Value(data='key'), Separator(), Value(data='value#abcd'), Newline()]  # test with an indentSize of 3
        ),
        (
            '''
-  key: value''', [SequenceIndent(), Value(data='key'), Separator(), Value(data='value'), Newline()]  # test with an indentSize of 3
        ),
        ('-  key', [SequenceIndent(), Value(data='key'), Newline()]),
        (
            '''key:
   key1: value
   key2: value''', [
                Value(data='key'),
                Separator(),
                Newline(),
                Indent(),
                Value(data='key1'),
                Separator(),
                Value(data='value'),
                Newline(),
                Indent(),
                Value(data='key2'),
                Separator(),
                Value(data='value'),
                Newline()
            ]
        ),
        ('''-   -   blah''', [SequenceIndent(), SequenceIndent(), Value(data='blah'), Newline()]),
        ('''- - blah''', [SequenceIndent(), SequenceIndent(), Value(data='blah'), Newline()]),
        ('''key:
key2:''', [Value(data='key'), Separator(), Newline(), Value(data='key2'), Separator(), Newline()]
        ),
        ('''
- key: value
- key2:
    key3: value
- value''',
            [
                SequenceIndent(), Value(data='key'), Separator(), Value(data='value'), Newline(),
                SequenceIndent(), Value(data='key2'), Separator(), Newline(),
                Indent(), Indent(), Value(data='key3'), Separator(), Value(data='value'), Newline(),
                SequenceIndent(), Value(data='value'), Newline(),
            ]
        )
    ])
    def test_key_value(self, string, expectedTokens):
        self.assertEqual(
            tokenize(string=string),
            expectedTokens,
        )

    @parameterized.expand([
        (' key', Exception),
    ])
    def test_key_value(self, string, expectedException):
        with self.assertRaises(expected_exception=expectedException):
            tokenize(string=string)
