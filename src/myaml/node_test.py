import unittest

from parameterized import parameterized

from .parser import Node
from .node_types import NodeTypes


class NodeTestCase(unittest.TestCase):
    pass


class TestFromStringNode(NodeTestCase):

    def test_scalar(self):
        string = 'value'
        node = Node.from_string(string=string)
        expectedNode = Node(nodeType=NodeTypes.SCALAR, value=string)
        self.assertEqual(node, expectedNode)

    def test_sequence(self):
        string = '''-   value
-   value2
-   key: value'''
        node = Node.from_string(string=string)
        expectedNode = Node(
            nodeType=NodeTypes.SEQUENCE,
            value=string,
            innerNodes=[
                Node(nodeType=NodeTypes.SCALAR, value='    value'),
                Node(nodeType=NodeTypes.SCALAR, value='    value2'),
                Node(
                    nodeType=NodeTypes.MAPPING,
                    value='    key: value',
                    innerNodes=[
                        
                    ]
                ),
            ]
        )
        self.assertEqual(node, expectedNode)

    def test_mapping(self):
        string = '''key: value
key2: value2'''
        node = Node.from_string(string=string)
        expectedNode = Node(
            nodeType=NodeTypes.MAPPING,
            value=string,
            innerNodes=[
                Node(nodeType=NodeTypes.SCALAR, value='key: value'),
                Node(nodeType=NodeTypes.SCALAR, value='key2: value2'),
            ]
        )
        self.assertEqual(node, expectedNode)

    # @parameterized.expand([
    #     ('''''', {})
    # ])
    # def test_complex_mapping(self, string, expected):
    #     self.assertEqual(Node.from_string(string=string), Node(nodeType=NodeTypes.MAPPING, value=string))


class TestToNativeObject(NodeTestCase):
    pass


class TestgetNodeType(NodeTestCase):

    @parameterized.expand([
        ('''this is a value''', NodeTypes.SCALAR),
        ('''key: ''', NodeTypes.MAPPING),
        ('''key:''', NodeTypes.MAPPING),
        ('''    key: ''', NodeTypes.MAPPING),
        ('''key: value''', NodeTypes.MAPPING),
        ('''key:
    key2: value''', NodeTypes.MAPPING),
        ('''- value
- value2
- value4''', NodeTypes.SEQUENCE),
        ('''- value
- key: value2
- value4''', NodeTypes.SEQUENCE),
    ])
    def test__get_node_type(self, string, expected):
        self.assertEqual(Node._get_node_type(string=string), expected)


class TestgetKeyValueStrings(NodeTestCase):
    def test_get_key_value_strings(self):
        string = '''key: value
key2: value
    key3: value
key3:
    - value
    - value2'''
        keyValueStrings = [
            '''key: value''',
            '''key2: value
    key3: value''',
            '''key3:
    - value
    - value2''',
        ]
        self.assertEqual(Node._get_key_value_strings(string=string), keyValueStrings)


class TestGetKeyString(NodeTestCase):
    @parameterized.expand([
        ('''key: value''', 'key'),
        ('''key:
- value''', 'key'),
        ('''key:
    key2: value''', 'key'),
        ('''key:
''', 'key')
    ])
    def test_get_key(self, string, expected):
        node = Node(
            value=string,
            nodeType=NodeTypes.MAPPING,
            innerNodes=[]
        )
        self.assertEqual(node.get_key_string(), expected)


class TestGetValueString(NodeTestCase):
    @parameterized.expand([
        ('''key: value''', 'value'),
        ('''key:
    key2: value''', '    key2: value'),
        ('''key:
''', '')
    ])
    def test_get_value(self, string, expected):
        node = Node(
            value=string,
            nodeType=NodeTypes.MAPPING,
            innerNodes=[]
        )
        self.assertEqual(node.get_value_string(), expected)


class TestgetElementStrings(NodeTestCase):
    @parameterized.expand([
        ('''-   key: value''', ['    key: value']),
        ('''-   value
-   key2: value''', [
    '''    value''',
    '''    key2: value'''
]),
    ])
    def test_get_value(self, string, expected):
        self.assertEqual(Node._get_element_strings(string=string), expected)
