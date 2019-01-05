from .exceptions import ParsingException
from .node_parsers import ArrayElementParser
from .node_parsers import KeyParser
from .node_parsers import KeyValueParser
from .node_types import NodeTypes
from .text import Text


class DictParser:

    def __init__(self):
        self._keyValueParser = KeyValueParser()
        self._keyParser = KeyParser()
        self._arrayElementParser = ArrayElementParser()

    def parse(self, text):
        currentNodeType = self._get_node_type(line=text.get_current_line())
        if currentNodeType in (NodeTypes.KEY, NodeTypes.KEY_VALUE):
            res = {}
            while not text.is_end_of_current_block():
                if currentNodeType == NodeTypes.KEY:
                    key = self._keyParser.parse(line=text.get_current_line())  # potentially a bad name
                    text.advance()
                    value = self.parse(text=text)
                    res[key] = value
                elif currentNodeType == NodeTypes.KEY_VALUE:
                    key, value = self._keyValueParser.parse(line=text.get_current_line())
                    text.advance()
                    res[key] = value
                else:
                    raise ParsingException(f'unrecognized node type for this line. line: {text.get_current_line()}')
            return res
        elif currentNodeType in (NodeTypes.ARRAY_ELEMENT):
            res = []
            # while not text.is_end_of_current_block():
            #     value = self._arrayElementParser.consume(text=text)
            #     # should I move the advance here so it is explicit?
            #     res.append(value)
            return res
        else:
            raise ParsingException(f'unrecognized node type for this line. line: {text.get_current_line()}')

    def _get_node_type(self, line):
        if self._keyParser.is_type(line=line):
            return NodeTypes.KEY
        elif self._keyValueParser.is_type(line=line):
            return NodeTypes.KEY_VALUE
        elif self._arrayElementParser.is_type(line=line):
            return NodeTypes.ARRAY_ELEMENT
        else:
            raise ParsingException(f'Unknown node type for this line. line: {line}')
