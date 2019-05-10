
class MyamlException(Exception):
    pass


class ParsingException(MyamlException):
    pass


class InconsistentIndentation(MyamlException):
    pass


class TokenizationException(MyamlException):
    def __init__(self, msg, context):
        super().__init__(msg)
        self.msg = msg
        self.context = context

    def __str__(self):
        line_number = self.context['line_number']
        column_number = self.context['column_number']
        return f'This error: "{self.msg}" occurred at line {line_number}, column {column_number}'
