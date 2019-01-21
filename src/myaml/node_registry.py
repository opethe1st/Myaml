
class NodeRegistry:

    _items = []

    def __init__(self):
        raise NotImplementedError

    @classmethod
    def register(cls, nodeCls: 'Node'):
        cls._items.append(nodeCls)

    @staticmethod
    def get_node_classes() -> list:
        return NodeRegistry._items


nodeRegistry = NodeRegistry
