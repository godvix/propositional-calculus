from parser import Parser


parser = Parser()


def infix_to_postfix(infix_split: list) -> list:
    return parser.parse(infix_split)


def postfix_to_prefix(postfix_list: list) -> list:
    unary = ["!"]
    binary = ["&", "|", "^", "~"]
    stack = []
    for token in postfix_list:
        if token in unary:
            new_expression = [token] + stack[-1]
            del stack[-1]
        elif token in binary:
            new_expression = [token] + stack[-2] + stack[-1]
            del stack[-2:]
        else:  # token is an operand
            new_expression = [token]
        stack.append(new_expression)
    assert len(stack) == 1
    return stack[0]


if __name__ == "__main__":
    infix_str = input("infix expression: ")
    try:
        infix_split = parser.tokenize(infix_str)
        postfix_list = infix_to_postfix(infix_split)
        prefix_list = postfix_to_prefix(postfix_list)
    except Exception as e:
        print(e)
    else:
        print(f"prefix expression: {' '.join(prefix_list)}")
        print(f"postfix expression: {' '.join(postfix_list)}")
