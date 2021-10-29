from naive_converter import OPERATORS
from parser import Parser


class Converter(object):
    def __init__(self) -> None:
        super().__init__()
        self.parser = Parser()
        self.operators = OPERATORS

    def tokenize(self, string: str) -> list:
        return self.parser.tokenize(string)

    def list_to_str(self, tokens: list) -> str:
        return " ".join(tokens)

    def infix_to_postfix(self, infix_tokens: list) -> list:
        return self.parser.parse(infix_tokens)

    def infix_to_prefix(self, infix_tokens: list) -> list:
        postfix_tokens = self.infix_to_postfix(infix_tokens)
        return self.postfix_to_prefix(postfix_tokens)

    def postfix_to_prefix(self, postfix_tokens: list) -> list:
        stack = list()
        print(postfix_tokens)
        for token in postfix_tokens:
            if token in self.operators:
                num_operands = self.operators[token].num_operands
                new_expression = [token] + sum(stack[-num_operands:], start=list())
                del stack[-num_operands:]
            else:  # token is an operand
                new_expression = [token]
            stack.append(new_expression)
        assert len(stack) == 1
        return stack[0]


if __name__ == "__main__":
    infix_str = input("infix expression: ")
    try:
        converter = Converter()
        infix_tokens = converter.tokenize(infix_str)
        postfix_tokens = converter.infix_to_postfix(infix_tokens)
        prefix_tokens = converter.postfix_to_prefix(postfix_tokens)
    except Exception as e:
        print(e)
    else:
        print("prefix expression:", converter.list_to_str(prefix_tokens))
        print("postfix expression:", converter.list_to_str(postfix_tokens))
