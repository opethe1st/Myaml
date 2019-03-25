import re
import string
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from dataclasses import dataclass


def tokenize(string):
    indentSize = get_indent_size(string=string)
    currentState = StartState(context={'indentSize': indentSize})
    allTokens = []
    characters = list(string)
    characters.append(None) # None indicates the end of the string
    for letter in characters:
        currentState, tokens = currentState.transition(inp=letter)
        allTokens.extend(tokens)
    return allTokens


def get_indent_size(string: str) -> Optional[int]:
    match = re.search(pattern=r'\n*^([-|\s]\s+)\S', string=string, flags=re.MULTILINE)
    indentSize = None
    if match:
        indentSize = len(match.group(1))
    return indentSize


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
            return StartState(context=self.context), [] # trims the trailing newlines.
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
        elif inp is None:
            return EndState(), [Value(data=self.tokenSoFar)]
        elif inp == '\n':
            return StartState(context=self.context), [Value(data=self.tokenSoFar), Newline()]
        elif inp == ' ':
            return SpaceState(context=self.context, count=1, tokenSoFar=self.tokenSoFar), []
        else:
            return CharacterState(context=self.context, tokenSoFar=self.tokenSoFar+inp), []
        raise Exception(f'this transisiton is not supported yet. inp: "{inp}"')


@dataclass
class ColonState(State):
    context: dict
    tokenSoFar: str
    def transition(self, inp):
        if inp == ' ':
            return StartState(context=self.context), [Value(data=self.tokenSoFar), Separator()]
        if inp == '\n':
            return StartState(context=self.context), [Value(data=self.tokenSoFar), Separator(), Newline()]
        else:
            return CharacterState(context=self.context, tokenSoFar=self.tokenSoFar+':'+inp), []
        raise Exception(f'this transisiton is not supported yet. inp: "{inp}"')


@dataclass
class SpaceState(State):
    context: dict
    count: int
    tokenSoFar: str = ''
    def transition(self, inp):
        indentSize = self.context.get('indentSize')
        if inp == ' ':
            if self.count == (indentSize-1):
                return SpaceState(context=self.context, count=0, tokenSoFar=self.tokenSoFar), [Indent()]
            else:
                return SpaceState(context=self.context, count=(self.count+1)%indentSize, tokenSoFar=self.tokenSoFar), []
        elif inp == '#':
            if self.tokenSoFar:
                return CommentState(context=self.context), [Value(data=self.tokenSoFar)]
            else:
                return CommentState(context=self.context), []
        elif inp is None:
            return EndState(), []
        else:
            if self.count == 0:
                if inp == '-':
                    return DashState(context=self.context), []
                else:
                    return CharacterState(context=self.context, tokenSoFar=inp), []
            else:
                raise Exception('Inconsistent Indentation')


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
            return SequenceIndentState(context=self.context, count=self.count+1), []
        else:
            if self.count == self.context.get('indentSize'):
                return CharacterState(context=self.context, tokenSoFar=inp), [SequenceIndent()]
            else:
                raise Exception('inconsistent sequence indentation')



@dataclass
class CommentState(State):
    context: dict
    tokenSoFar: str = ''
    def transition(self, inp):
        if (inp == '\n') or (inp is None):
            return StartState(context=self.context), []
        else:
            return CommentState(context=self.context), []  # actually could make this self, [] - but using CommentState to be consistent with the others


@dataclass
class EndState(State):
    def transition(self, inp):
        pass


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
