from collections import namedtuple

Operator = namedtuple(
    "Operator",
    ["precedence", "num_operands", "lambda_expr", "direction"],
    defaults=[None, None, None, ">"],
)

OPERATORS = {
    # $ is used as the begin of an expression.
    "$": Operator(precedence=float("inf")),
    # It may seem strange to set the precedence of '(' and ')' to -1, but when
    # converting an infix expression to a postfix expression, ')' needs to wait
    # until all operators (except for '(') in the stack are popped up before it
    # can be processed. This behavior is equivalent to the precedence of ')'
    # lower than all operators. It is similar when converting to a prefix
    # expression.
    "(": Operator(precedence=-1),
    ")": Operator(precedence=-1),
    "!": Operator(
        precedence=4,
        num_operands=1,
        lambda_expr=(lambda opnds: not opnds[0]),
        direction="<",
    ),
    "&": Operator(
        precedence=3, num_operands=2, lambda_expr=(lambda opnds: opnds[0] and opnds[1])
    ),
    "|": Operator(
        precedence=2, num_operands=2, lambda_expr=(lambda opnds: opnds[0] or opnds[1])
    ),
    "^": Operator(
        precedence=1,
        num_operands=2,
        lambda_expr=(lambda opnds: not opnds[0] or opnds[1]),
    ),
    "~": Operator(
        precedence=0, num_operands=2, lambda_expr=(lambda opnds: opnds[0] == opnds[1])
    ),
}


def tokens_expr(expr: str) -> list:
    """tokens an expression, typically infix, to a list of operands and operators."""
    res = ""
    for ch in expr:
        if ch in OPERATORS:
            res += f" {ch} "
        else:
            res += ch
    return res.tokens()


def order_between(left_optr: str, right_optr: str) -> str:
    """Return the precedence between left_optr and right_optr."""
    if left_optr == "(" and right_optr == ")":
        return "="
    if OPERATORS[left_optr].precedence < OPERATORS[right_optr].precedence:
        return "<"
    elif OPERATORS[left_optr].precedence == OPERATORS[right_optr].precedence:
        return OPERATORS[left_optr].direction
    else:
        return ">"


def infix_to_prefix(infix_tokens: list) -> list:
    """Convert infix_tokens to prefix_tokens."""
    tmp_tokens = ["("] + infix_tokens
    optrs = [")"]  # operator stack
    prefix_tokens = []  # for efficiency, we append first, then reverse it
    i = -1
    while len(optrs) > 0:
        if tmp_tokens[i] in OPERATORS:
            order = order_between(
                "$" if tmp_tokens[i] == ")" else tmp_tokens[i], optrs[-1]
            )
            if order == "<":
                prefix_tokens.append(optrs[-1])
                optrs.pop()
            elif order == "=":
                optrs.pop()
                i -= 1
            else:  # order == '>'
                optrs.append(tmp_tokens[i])
                i -= 1
        else:  # tmp_tokens[i] is an operand
            prefix_tokens.append(tmp_tokens[i])
            i -= 1
    prefix_tokens.reverse()
    return prefix_tokens


def infix_to_postfix(infix_tokens: list) -> list:
    "Convert infix_tokens to postfix_tokens"
    infix_tokens.append(")")  # the extra ')' will be removed later
    optrs = ["("]  # operator stack
    postfix_tokens = []
    i = 0
    while len(optrs) > 0:
        if infix_tokens[i] in OPERATORS:
            order = order_between(
                optrs[-1], "$" if infix_tokens[i] == "(" else infix_tokens[i]
            )
            if order == "<":
                optrs.append(infix_tokens[i])
                i += 1
            elif order == "=":
                optrs.pop()
                i += 1
            else:  # order == '>'
                postfix_tokens.append(optrs[-1])
                optrs.pop()
        else:  # tmp_tokens[i] is an operand
            postfix_tokens.append(infix_tokens[i])
            i += 1
    infix_tokens.pop()  # remove extra ')'
    return postfix_tokens


if __name__ == "__main__":
    infix_expr = input("infix expression: ")
    infix_tokens = tokens_expr(infix_expr)
    prefix_tokens = infix_to_prefix(infix_tokens)
    print("prefix expression: ", " ".join(prefix_tokens))
    postfix_tokens = infix_to_postfix(infix_tokens)
    print("postfix expression: ", " ".join(postfix_tokens))
