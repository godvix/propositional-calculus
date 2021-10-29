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


def split_expr(expr: str) -> list:
    """Split an expression, typically infix, to a list of operands and operators."""
    res = ""
    for ch in expr:
        if ch in OPERATORS:
            res += f" {ch} "
        else:
            res += ch
    return res.split()


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


def infix_to_prefix(infix_split: list) -> list:
    """Convert infix_split to prefix_split."""
    tmp_split = ["("] + infix_split
    optrs = [")"]  # operator stack
    prefix_split = []  # for efficiency, we append first, then reverse it
    i = -1
    while len(optrs) > 0:
        if tmp_split[i] in OPERATORS:
            order = order_between(
                "$" if tmp_split[i] == ")" else tmp_split[i], optrs[-1]
            )
            if order == "<":
                prefix_split.append(optrs[-1])
                optrs.pop()
            elif order == "=":
                optrs.pop()
                i -= 1
            else:  # order == '>'
                optrs.append(tmp_split[i])
                i -= 1
        else:  # tmp_split[i] is an operand
            prefix_split.append(tmp_split[i])
            i -= 1
    prefix_split.reverse()
    return prefix_split


def infix_to_postfix(infix_split: list) -> list:
    "Convert infix_split to postfix_split"
    infix_split.append(")")  # the extra ')' will be removed later
    optrs = ["("]  # operator stack
    postfix_split = []
    i = 0
    while len(optrs) > 0:
        if infix_split[i] in OPERATORS:
            order = order_between(
                optrs[-1], "$" if infix_split[i] == "(" else infix_split[i]
            )
            if order == "<":
                optrs.append(infix_split[i])
                i += 1
            elif order == "=":
                optrs.pop()
                i += 1
            else:  # order == '>'
                postfix_split.append(optrs[-1])
                optrs.pop()
        else:  # tmp_split[i] is an operand
            postfix_split.append(infix_split[i])
            i += 1
    infix_split.pop()  # remove extra ')'
    return postfix_split


if __name__ == "__main__":
    infix_expr = input("infix expression: ")
    infix_split = split_expr(infix_expr)
    prefix_split = infix_to_prefix(infix_split)
    print("prefix expression: ", " ".join(prefix_split))
    postfix_split = infix_to_postfix(infix_split)
    print("postfix expression: ", " ".join(postfix_split))
