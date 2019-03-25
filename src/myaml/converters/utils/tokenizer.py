import string
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from dataclasses import dataclass


def tokenize(string):
    currentState = StartState()
    allTokens = []
    characters = list(string)
    characters.append(None) # None indicates the end of the string
    for letter in characters:
        currentState, tokens = currentState.transition(inp=letter)
        allTokens.extend(tokens)
    return allTokens



# State machine
class State(ABC):
    @abstractmethod
    def transition(self, inp: str) -> Tuple['State', List['Token']]:
        pass


class StartState(State):
    def transition(self, inp):
        if inp == ' ':
            return SpaceState(count=1), []
        elif inp == '-':
            return DashState(), []
        else:
            return CharacterState(tokenSoFar=inp), []
        raise Exception(f'this transisiton is not supported yet. inp: "{inp}"')


@dataclass
class CharacterState(State):
    tokenSoFar: str
    def transition(self, inp) -> Tuple['State', List['Token']]:
        if inp == ':':
            return ColonState(tokenSoFar=self.tokenSoFar), []
        elif inp is None:
            return EndState(), [Value(data=self.tokenSoFar)]
        elif inp == '\n':
            return StartState(), [Value(data=self.tokenSoFar), Newline()]
        else:
            return CharacterState(tokenSoFar=self.tokenSoFar+inp), []
        raise Exception(f'this transisiton is not supported yet. inp: "{inp}"')


@dataclass
class ColonState(State):
    tokenSoFar: str
    def transition(self, inp):
        if inp == ' ':
            return StartState(), [Value(data=self.tokenSoFar), Separator()]
        if inp == '\n':
            return StartState(), [Value(data=self.tokenSoFar), Separator(), Newline()]
        else:
            return CharacterState(tokenSoFar=self.tokenSoFar+':'+inp), []
        raise Exception(f'this transisiton is not supported yet. inp: "{inp}"')


@dataclass
class SpaceState(State):
    count: int
    def transition(self, inp):
        if inp == ' ':
            if self.count == 1:  # for now assuming the indent is 2
                return SpaceState(count=0), [Indent()]
            else:
                return SpaceState(count=self.count+1), []
        else:
            if self.count == 0:
                if inp == '-':
                    return DashState(), []
                else:
                    return CharacterState(tokenSoFar=inp), []
            else:
                raise Exception('Inconsistent Indentation')


@dataclass
class DashState(State):
    def transition(self, inp):
        if inp == ' ':
            return SequenceIndentState(count=2), []
        else:
            return CharacterState(tokenSoFar=f'-{inp}'), []


@dataclass
class SequenceIndentState(State):
    count: int
    def transition(self, inp):
        if inp == ' ':
            return SequenceIndentState(count=self.count+1), []
        else:
            if self.count == 2: # two is the what we are assuming all the indents are.
                return CharacterState(tokenSoFar=inp), [SequenceIndent()]
            else:
                raise Exception('inconsistent sequence indentation')



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
