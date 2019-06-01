from unittest import TestCase

from myaml.loading.line import Line, lines_from_tokens
from myaml.loading.tokenizer import (
    Indent,
    Newline,
    Separator,
    SequenceIndent,
    Token,
    Value
)


class TestIsScalar(TestCase):

    def test_is_scalar(self):
        line = Line(indent=0, tokens=[Value(data='value')])
        self.assertTrue(line.is_scalar())
        self.assertFalse(line.is_mapping())
        self.assertFalse(line.is_sequence())


class TestIsMapping(TestCase):

    def test_is_mapping(self):
        line = Line(indent=0, tokens=[Value(data='value'), Separator()])
        self.assertTrue(line.is_mapping())
        self.assertFalse(line.is_scalar())
        self.assertFalse(line.is_sequence())


class TestIsSequence(TestCase):

    def test_is_sequence(self):
        line = Line(indent=0, tokens=[SequenceIndent(), Value(data='value'), Separator()])
        self.assertTrue(line.is_sequence())
        self.assertFalse(line.is_mapping())
        self.assertFalse(line.is_scalar())



class TestLinesFromTokens(TestCase):

    def test_lines_from_tokens(self):
        tokens = [
            Value(data='key'), Separator(), Newline(),
            Indent(), Value(data='key1'), Separator(), Value(data='value')
        ]
        lines = lines_from_tokens(tokens=tokens)
        self.assertEqual(
            lines,
            [
                Line(indent=0, tokens=[Value(data='key'), Separator()]),
                Line(indent=1, tokens=[Value(data='key1'), Separator(), Value(data='value')])
            ]
        )
