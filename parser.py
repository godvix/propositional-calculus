from collections import namedtuple
import re
import sys
import grammar

Token = namedtuple(
    typename="Token", field_names=["symbol", "value"], defaults=[None, None]
)

Step = namedtuple(
    typename="Step", field_names=["state", "token"], defaults=[None, None]
)


class Parser:
    def __init__(self) -> None:
        self.tokens = dict()
        self.rules = grammar.rules
        for key, value in grammar.tokens.items():
            self.tokens[key] = re.compile(value)
        self.transition_table = grammar.transition_table

    def tokenize(self, input: str) -> list:
        pos = 0
        tokens = []
        while pos < len(input):
            for key, value in self.tokens.items():
                match = value.match(input, pos)
                if match is not None:
                    pos = match.end()
                    if key != "ignore":
                        tokens.append(Token(symbol=key, value=match.group()))
                    break
            else:
                raise Exception(f"Illegal character {input[pos]}")
        tokens.append(Token(symbol="$", value="EOF"))
        return tokens

    def parse(self, tokens: list, debug: bool = False, debug_file=sys.stderr):
        tokens.reverse()
        stack = [Step(state=0)]
        while len(tokens) > 0:
            token = tokens[-1]
            state = stack[-1].state
            expectation = self.transition_table[state]
            if debug:
                print(f"State  : {state}", file=debug_file)
                print(f"Stack  : {stack} . {token}", file=debug_file)
            if token.symbol in expectation:
                action = expectation[token.symbol]
                if action[0] == "s":  # shift and go to state action[1]
                    tokens.pop()
                    stack.append(Step(state=action[1], token=token))
                    state = action[1]
                    if debug:
                        print(
                            f"Action : Shift and goto state {action[1]}",
                            file=debug_file,
                        )
                elif action[0] == "r":  # reduce using rule action[1]
                    rule = self.rules[action[1]]
                    p = [None]
                    for i in range(-len(rule.body), 0):
                        p.append(stack[i].token.value)
                    del stack[-len(rule.body) :]
                    state = stack[-1].state
                    if rule.method is not None:
                        rule.method(p)
                    tokens.append(Token(symbol=rule.head, value=p[0]))
                    if debug:
                        print(
                            f"Action : Reduce rule [{rule.head} -> {' '.join(rule.body)}] with {p[1:]}",
                            file=debug_file,
                        )
                elif action[0] == "t":  # terminate
                    assert len(tokens) == 1
                    assert tokens[0].symbol == "$"
                    assert len(stack) == 2
                    return stack[1].token.value
                else:
                    assert False
            else:
                raise Exception(
                    f"Expect {list(expectation.keys())} but found {token.value} instead"
                )


if __name__ == "__main__":
    parser = Parser()
    str = input("infix expression: ")
    try:
        infix_split = parser.tokenize(str)
        postfix_split = parser.parse(infix_split)
    except Exception as e:
        print(e.args)
    else:
        print(" ".join(postfix_split))
