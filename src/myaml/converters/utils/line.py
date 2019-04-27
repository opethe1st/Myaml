from typing import List

from dataclasses import dataclass

from .tokenizer import Indent, Newline, Separator, SequenceIndent, Token, Value


@dataclass
class Line:
    indent: int
    tokens: List['Token']

    # TODO(ope): is this the right model? the model where lines have types?
    def is_scalar(self):
        if len(self.tokens) == 1:
            return isinstance(self.tokens[0], Value)
        return False

    def is_mapping(self):
        if len(self.tokens) > 1:
            return all([
                isinstance(self.tokens[0], Value),
                isinstance(self.tokens[1], Separator),
            ])
        return False

    def is_sequence(self):
        if len(self.tokens) > 1:
            return isinstance(self.tokens[0], SequenceIndent)
        return False

# TODO(ope), pass in a reference to all the tokens and the bounds instead of the slic of the tokens
def line_from_tokens(tokens):
    indent = 0
    position = 0
    while position < len(tokens) and isinstance(tokens[position], Indent): # should I include the SequenceIndent?
        indent += 1
        position += 1
    if position < len(tokens) and isinstance(tokens[position], SequenceIndent):
        indent+=1
    return Line(indent=indent, tokens=tokens[position:])


def lines_from_tokens(tokens):
    lines = []
    currentTokens = []
    position = 0
    while position < len(tokens):
        if not isinstance(tokens[position], Newline):
            currentTokens.append(tokens[position])
        else:
            if currentTokens:
                lines.append(line_from_tokens(tokens=currentTokens))
            currentTokens = []
        position += 1
    if currentTokens:
        lines.append(line_from_tokens(tokens=currentTokens))
    return lines
