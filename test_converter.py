from converter import infix_to_postfix, postfix_to_prefix
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
    postfix_list = infix_to_postfix(infix_str)
    assert " ".join(postfix_list) == postfix_str
    prefix_list = postfix_to_prefix(postfix_list)
    assert " ".join(prefix_list) == prefix_str
