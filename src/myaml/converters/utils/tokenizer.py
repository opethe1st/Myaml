import re
import string
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from dataclasses import dataclass

from myaml.exceptions import InconsistentIndentation


def tokenize(string):
    string = string.rstrip()+'\n'
    indentSize = get_indent_size(string=string)
    currentState = StartState(context={'indentSize': indentSize})
    allTokens = []
    for line in string.splitlines(keepends=True):
        tokensOnLine = []
        for letter in line:
            currentState, tokens = currentState.transition(inp=letter)
            tokensOnLine.extend(tokens)
        if tokensOnLine and not all(isinstance(token, (SequenceIndent, Indent)) for token in tokensOnLine):
            allTokens.extend(tokensOnLine)
    return allTokens


def get_indent_size(string: str) -> Optional[int]:
    match = re.search(pattern=r'\n*^([-|\s]\s+)(?!#)\S', string=string, flags=re.MULTILINE)
    indentSize = None
    if match:
        indentSize = len(match.group(1))
    return indentSize

#  Turns out I could have avoided all of this low-level state machine business if I just used regex.
# Would it be faster with regex? Experiment with it later.

# State machine
class State(ABC):
    @abstractmethod
    def transition(self, inp: str) -> Tuple['State', List['Token']]:
        pass


@dataclass
class StartState(State):
    context: dict
    def transition(self, inp):
        if inp == ' ':
            return SpaceState(context=self.context, count=1), []
        elif inp == '-':
            return DashState(context=self.context), []
        elif inp == '#':
            return CommentState(context=self.context, tokenSoFar=''), []
        elif inp == '\n':
            return self, [] # trims the trailing newlines.
        else:
            return CharacterState(context=self.context, tokenSoFar=inp), []
        raise Exception(f'this transisiton is not supported yet. inp: "{inp}"')


@dataclass
class CharacterState(State):
    context: dict
    tokenSoFar: str
    def transition(self, inp) -> Tuple['State', List['Token']]:
        if inp == ':':
            return ColonState(context=self.context, tokenSoFar=self.tokenSoFar), []
        elif inp == '\n':
            return StartState(context=self.context), [Value(data=self.tokenSoFar), Newline()]
        elif inp == ' ':
            return SpaceInCharacterState(context=self.context, tokenSoFar=self.tokenSoFar), []
        else:
            self.tokenSoFar += inp
            return self, []
        raise Exception(f'this transisiton is not supported yet. inp: "{inp}"')


@dataclass
class ColonState(State):
    context: dict
    tokenSoFar: str
    def transition(self, inp):
        if inp == ' ':
            return StartState(context=self.context), [Value(data=self.tokenSoFar), Separator()]
        elif inp == '\n':
            return StartState(context=self.context), [Value(data=self.tokenSoFar), Separator(), Newline()]
        else:
            return CharacterState(context=self.context, tokenSoFar=self.tokenSoFar+':'+inp), []


@dataclass
class SpaceInCharacterState(State):
    context: dict
    tokenSoFar: str
    def transition(self, inp):
        if inp == '#':
            return CommentState(context=self.context), [Value(data=self.tokenSoFar)]
        else:
            return CharacterState(context=self.context, tokenSoFar=self.tokenSoFar+' '+inp), []


@dataclass
class SpaceState(State):
    context: dict
    count: int
    def transition(self, inp):
        indentSize = self.context.get('indentSize')
        if inp == ' ':
            self.count = (self.count+1)%indentSize
            if self.count == 0:
                return self, [Indent()]
            else:
                return self, []
        elif inp == '#':
            return CommentState(context=self.context), []
        else:
            if self.count == 0:
                if inp == '-':
                    return DashState(context=self.context), []
                else:
                    return CharacterState(context=self.context, tokenSoFar=inp), []
            else:
                raise InconsistentIndentation(f'Inconsistent Indentation')


@dataclass
class DashState(State):
    context: str
    def transition(self, inp):
        if inp == ' ':
            return SequenceIndentState(context=self.context, count=2), []  # this is 2 because '- ' have been consumed so far.
        else:
            return CharacterState(context=self.context, tokenSoFar=f'-{inp}'), []


@dataclass
class SequenceIndentState(State):
    context: dict
    count: int
    def transition(self, inp):
        if inp == ' ':
            self.count = self.count + 1
            return self, []
        else:
            if self.count == self.context.get('indentSize'):
                if inp == '-':
                    return DashState(context=self.context), [SequenceIndent()]
                else:
                    return CharacterState(context=self.context, tokenSoFar=inp), [SequenceIndent()]
            else:
                raise Exception('inconsistent sequence indentation')


@dataclass
class CommentState(State):
    context: dict
    tokenSoFar: str = ''
    def transition(self, inp):
        if inp == '\n':
            return StartState(context=self.context), []
        else:
            return self, []


# Token types
class Token:
    pass

@dataclass
class Value(Token):
    data: str


@dataclass
class Separator(Token):
    pass


@dataclass
class Indent(Token):
    pass


@dataclass
class Newline(Token):
    pass


@dataclass
class SequenceIndent(Token):
    pass
