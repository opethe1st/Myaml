import re

from .exceptions import ParsingException


class Text:

    def __init__(self, lines):
        self.lines = lines
        self._current_cursor = 0
        self._current_block_cursor = 0
        self._current_indent_level = self._get_indent_level(lines[0])
        self._indent = 2
        self._get_indent_regex = None

    def get_current_line(self):
        return self.lines[self._current_cursor] if self._current_cursor < len(self.lines) else None

    def advance(self):
        self._current_cursor += 1

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

    def is_end_of_current_block(self):
        return self._current_cursor >= len(self.lines)
