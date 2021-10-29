from naive_converter import OPERATORS
from prettytable import PrettyTable
from converter import Converter


class Evaluator(object):
    def __init__(self) -> None:
        super().__init__()
        self.operators = OPERATORS
        self.false_constants = ["0", "F", "False", "false"]
        self.true_constants = ["1", "T", "True", "true"]

    def get_operand_symbols(self, tokens: list) -> list:
        symbols_set = set()
        for op in tokens:
            if (
                (op not in self.operators)
                and (op not in self.false_constants)
                and (op not in self.true_constants)
            ):
                symbols_set.add(op)
        result = list(symbols_set)
        result.sort()
        return result

    def get_truth_table(self, postfix_tokens: list) -> list:
        operands = dict().fromkeys(self.get_operand_symbols(postfix_tokens), False)
        result = list()
        for i in range(1 << len(operands)):
            row = list()
            values_str = bin(i)[2:].zfill(len(operands))
            for index, key in enumerate(operands.keys()):
                operands[key] = bool(int(values_str[index]))
                row.append(int(operands[key]))
            operand_stack = []
            for token in postfix_tokens:
                if token in self.operators:
                    operator = self.operators[token]
                    operand_values = operand_stack[-operator.num_operands :]
                    del operand_stack[-operator.num_operands :]
                    operand_stack.append(operator.lambda_expr(operand_values))
                elif token in self.false_constants:
                    operand_stack.append(False)
                elif token in self.true_constants:
                    operand_stack.append(True)
                else:
                    operand_stack.append(operands[token])
            row.append(int(operand_stack[0]))
            result.append(row)
        return list(operands.keys()) + ["result"], result


def truth_table_to_principal_disjunctive_normal_form(truth_table: list) -> list:
    result = list()
    for index, row in enumerate(truth_table):
        if row[-1] == 1:
            result.append(index)
    return result


def truth_table_to_principal_conjunctive_normal_form(truth_table: list) -> list:
    result = list()
    for index, row in enumerate(truth_table):
        if row[-1] == 0:
            result.append(len(truth_table) - index - 1)
    result.reverse()
    return result


if __name__ == "__main__":
    infix_str = input("infix expression: ")
    try:
        converter = Converter()
        infix_tokens = converter.tokenize(infix_str)
        postfix_tokens = converter.infix_to_postfix(infix_tokens)
    except Exception as e:
        print(e)
    else:
        evaluator = Evaluator()
        operand_symbols, truth_table = evaluator.get_truth_table(postfix_tokens)
        pretty_table = PrettyTable(operand_symbols)
        pretty_table.add_rows(truth_table)
        print(pretty_table)
        print(
            "principal disjunctive normal form:",
            truth_table_to_principal_disjunctive_normal_form(truth_table),
        )
        print(
            "principal conjunctive normal form:",
            truth_table_to_principal_conjunctive_normal_form(truth_table),
        )
