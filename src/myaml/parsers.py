import re

from .exceptions import ParsingException


class ArrayParser:

    def parse(self, text):
        res = []
        while text.has_next_block():
            text.advance()
            block = text.get_current_block()
            value = parse_text(text=block)
            res.append(value)
        return res


class DictParser:

    def parse(self, text):
        res = {}
        while text.has_next_block():
            text.advance()
            block = text.get_current_block()
            key, value = parse_text(text=block)
            res[key] = value
        return res


class Text:

    def __init__(self, lines):
        self._lines = lines[:]
        self._cursor = 0
        self._get_indent_regex = None
        self._indent = 2

    def get_current_block(self):
        if self._cursor > len(self._lines):
            return None
        line = self._lines[self._cursor]
        current_indent_level = self._get_indent_level(line=line)
        line_index = 0
        sublines = []
        while (line_index < len(self._lines)
                and self._get_indent_level(line=self._lines[line_index]) > current_indent_level):
            sublines.append(self._lines[line_index])
            line_index += 1
        return Text(lines=sublines)

    def has_next_block(self):
        return self._cursor < len(self._lines)

    def _get_indent_level(self, line: str):
        if self._get_indent_regex is None:
            self._get_indent_regex = re.compile(pattern=r'^(([ ]*)\w)|^')
        match = self._get_indent_regex.search(string=line)
        if match.group(2) is not None:
            number_of_spaces = len(match.group(2))
            indent_level = number_of_spaces / self._indent
            # might make this a function so my code is more self documenting - checks if a number is an integer
            if int(indent_level) != indent_level:
                raise ParsingException(f'Expected a multiple of {self._indent} as the indent but got {number_of_spaces}')
        else:
            raise ParsingException(rf'''The line didn't match the pattern. line: "{line}". pattern: "^(([ ]*)\w)|^"''')
        return indent_level


def parse_text(text):
    if text.nodeType == 'KEY_VALUE':

        return 'key', 'value'
    if text.nodeType == 'KEY':

        return 'key'
