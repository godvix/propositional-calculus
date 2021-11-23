from parser import Parser
from converter import Converter
import pytest

testdata = [
    ("!(P & Q)", "! & P Q", "P Q & !"),
    ("!P | !Q", "| ! P ! Q", "P ! Q ! |"),
    ("P ^ Q", "^ P Q", "P Q ^"),
    ("!P | Q", "| ! P Q", "P ! Q |"),
    ("!!P", "! ! P", "P ! !"),
    ("!P ~ Q", "~ ! P Q", "P ! Q ~"),
    ("!(P | Q)", "! | P Q", "P Q | !"),
    ("!P & !Q", "& ! P ! Q", "P ! Q ! &"),
    ("!(P & Q)", "! & P Q", "P Q & !"),
    ("(!P | Q) & (P | !Q)", "& | ! P Q | P ! Q", "P ! Q | P Q ! | &"),
    ("(P & Q) | (!P & !Q)", "| & P Q & ! P ! Q", "P Q & P ! Q ! & |"),
    ("(P ^ Q) & !(P ~ Q)", "& ^ P Q ! ~ P Q", "P Q ^ P Q ~ ! &"),
    ("P ^ Q", "^ P Q", "P Q ^"),
    ("!Q ^ !P", "^ ! Q ! P", "Q ! P ! ^"),
    ("!P ^ !Q", "^ ! P ! Q", "P ! Q ! ^"),
    ("Q ^ P", "^ Q P", "Q P ^"),
    ("P ^ (Q ^ R)", "^ P ^ Q R", "P Q R ^ ^"),
    ("P & Q ^ R", "^ & P Q R", "P Q & R ^"),
    ("P ^ P", "^ P P", "P P ^"),
    ("!((P | Q) ^ (Q | P))", "! ^ | P Q | Q P", "P Q | Q P | ^ !"),
    ("(Q ^ R) ^ ((P | Q) ^ (P | R))", "^ ^ Q R ^ | P Q | P R", "Q R ^ P Q | P R | ^ ^"),
    ("(Q ^ R) ^ ((P ^ Q) ^ (P ^ R))", "^ ^ Q R ^ ^ P Q ^ P R", "Q R ^ P Q ^ P R ^ ^ ^"),
    ("(P ^ Q) ^ (!Q ^ !P)", "^ ^ P Q ^ ! Q ! P", "P Q ^ Q ! P ! ^ ^"),
    ("(P & Q) ^ (P | Q)", "^ & P Q | P Q", "P Q & P Q | ^"),
    ("P ^ Q | R | S", "^ P | | Q R S", "P Q R | S | ^"),
    ("P & !R ~ P | Q", "~ & P ! R | P Q", "P R ! & P Q | ~"),
    ("!!P | (W & R) | !Q", "| | ! ! P & W R ! Q", "P ! ! W R & | Q ! |"),
    ("((P ^ !Q) ^ (Q ^ !P)) & R", "& ^ ^ P ! Q ^ Q ! P R", "P Q ! ^ Q P ! ^ ^ R &"),
    ("R", "R", "R"),
    (
        "(P ~ Q) ~ ((P & !Q) | (Q & !P))",
        "~ ~ P Q | & P ! Q & Q ! P",
        "P Q ~ P Q ! & Q P ! & | ~",
    ),
    ("P & !P", "& P ! P", "P P ! &"),
    ("!(P ~ Q)", "! ~ P Q", "P Q ~ !"),
    ("(P & !Q) | (!P & Q)", "| & P ! Q & ! P Q", "P Q ! & P ! Q & |"),
    ("A ^ B", "^ A B", "A B ^"),
    ("!B ^ !A", "^ ! B ! A", "B ! A ! ^"),
    ("A ~ B", "~ A B", "A B ~"),
    ("!A ~ !B", "~ ! A ! B", "A ! B ! ~"),
]


@pytest.mark.parametrize("infix_str, prefix_str, postfix_str", testdata)
def test_converter(infix_str, prefix_str, postfix_str):
    parser = Parser()
    infix_tokens = parser.tokenize(infix_str)
    converter = Converter()
    postfix_tokens = converter.infix_to_postfix(infix_tokens)
    assert " ".join(postfix_tokens) == postfix_str
    prefix_tokens = converter.postfix_to_prefix(postfix_tokens)
    assert " ".join(prefix_tokens) == prefix_str
