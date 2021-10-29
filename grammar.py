from collections import namedtuple


tokens = {
    "ignore": r"\s",
    "X": r"0|1|([a-zA-Z_][a-zA-Z0-9_]*)",
    "(": r"\(",
    ")": r"\)",
    "!": r"!",
    "|": r"\|",
    "&": r"\&",
    "^": r"\^",
    "~": r"~",
}


Rule = namedtuple(
    typename="Rule", field_names=["head", "body", "method"], defaults=[None, None, None]
)


def p_variable(p: list) -> None:
    """E : X"""
    p[0] = [p[1]]


def p_parens(p: list) -> None:
    """E : '(' E ')'"""
    p[0] = p[2]


def p_negation(p: list) -> None:
    """E : '!' E"""
    p[0] = p[2] + ["!"]


def p_binary_operation(p: list) -> None:
    """
    E : E '|' E
      | E '&' E
      | E '^' E
      | E '~' E
    """
    p[0] = p[1] + p[3] + [p[2]]


rules = {
    # Rule 0     S' -> E
    0: Rule(head="S'", body=["E"]),
    # Rule 1     E -> X
    1: Rule(head="E", body=["X"], method=p_variable),
    # Rule 2     E -> ( E )
    2: Rule(head="E", body=["(", "E", ")"], method=p_parens),
    # Rule 3     E -> ! E
    3: Rule(head="E", body=["!", "E"], method=p_negation),
    # Rule 4     E -> E & E
    4: Rule(head="E", body=["E", "&", "E"], method=p_binary_operation),
    # Rule 5     E -> E | E
    5: Rule(head="E", body=["E", "|", "E"], method=p_binary_operation),
    # Rule 6     E -> E ^ E
    6: Rule(head="E", body=["E", "^", "E"], method=p_binary_operation),
    # Rule 7     E -> E ~ E
    7: Rule(head="E", body=["E", "~", "E"], method=p_binary_operation),
}


# Terminals, with rules where they appear
# !                    : 3
# &                    : 4
# (                    : 2
# )                    : 2
# X                    : 1
# ^                    : 6
# error                :
# |                    : 5
# ~                    : 7

# Nonterminals, with rules where they appear
# E                    : 2 3 4 4 5 5 6 6 7 7 0


transition_table = {
    0: {  # state 0
        # (0) S' -> . E
        # (1) E -> . X
        # (2) E -> . ( E )
        # (3) E -> . ! E
        # (4) E -> . E & E
        # (5) E -> . E | E
        # (6) E -> . E ^ E
        # (7) E -> . E ~ E
        "X": ("s", 2),  # shift and go to state 2
        "(": ("s", 3),  # shift and go to state 3
        "!": ("s", 4),  # shift and go to state 4
        "E": ("s", 1),  # shift and go to state 1
    },
    1: {  # state 1
        # (0) S' -> E .
        # (4) E -> E . & E
        # (5) E -> E . | E
        # (6) E -> E . ^ E
        # (7) E -> E . ~ E
        "$": ("t",),  # terminate
        "&": ("s", 5),  # shift and go to state 5
        "|": ("s", 6),  # shift and go to state 6
        "^": ("s", 7),  # shift and go to state 7
        "~": ("s", 8),  # shift and go to state 8
    },
    2: {  # state 2
        # (1) E -> X .
        "&": ("r", 1),  # reduce using rule 1 (E -> X .)
        "|": ("r", 1),  # reduce using rule 1 (E -> X .)
        "^": ("r", 1),  # reduce using rule 1 (E -> X .)
        "~": ("r", 1),  # reduce using rule 1 (E -> X .)
        "$": ("r", 1),  # reduce using rule 1 (E -> X .)
        ")": ("r", 1),  # reduce using rule 1 (E -> X .)
    },
    3: {  # state 3
        # (2) E -> ( . E )
        # (1) E -> . X
        # (2) E -> . ( E )
        # (3) E -> . ! E
        # (4) E -> . E & E
        # (5) E -> . E | E
        # (6) E -> . E ^ E
        # (7) E -> . E ~ E
        "X": ("s", 2),  # shift and go to state 2
        "(": ("s", 3),  # shift and go to state 3
        "!": ("s", 4),  # shift and go to state 4
        "E": ("s", 9),  # shift and go to state 9
    },
    4: {  # state 4
        # (3) E -> ! . E
        # (1) E -> . X
        # (2) E -> . ( E )
        # (3) E -> . ! E
        # (4) E -> . E & E
        # (5) E -> . E | E
        # (6) E -> . E ^ E
        # (7) E -> . E ~ E
        "X": ("s", 2),  # shift and go to state 2
        "(": ("s", 3),  # shift and go to state 3
        "!": ("s", 4),  # shift and go to state 4
        "E": ("s", 10),  # shift and go to state 10
    },
    5: {  # state 5
        # (4) E -> E & . E
        # (1) E -> . X
        # (2) E -> . ( E )
        # (3) E -> . ! E
        # (4) E -> . E & E
        # (5) E -> . E | E
        # (6) E -> . E ^ E
        # (7) E -> . E ~ E
        "X": ("s", 2),  # shift and go to state 2
        "(": ("s", 3),  # shift and go to state 3
        "!": ("s", 4),  # shift and go to state 4
        "E": ("s", 11),  # shift and go to state 11
    },
    6: {  # state 6
        # (5) E -> E | . E
        # (1) E -> . X
        # (2) E -> . ( E )
        # (3) E -> . ! E
        # (4) E -> . E & E
        # (5) E -> . E | E
        # (6) E -> . E ^ E
        # (7) E -> . E ~ E
        "X": ("s", 2),  # shift and go to state 2
        "(": ("s", 3),  # shift and go to state 3
        "!": ("s", 4),  # shift and go to state 4
        "E": ("s", 12),  # shift and go to state 12
    },
    7: {  # state 7
        # (6) E -> E ^ . E
        # (1) E -> . X
        # (2) E -> . ( E )
        # (3) E -> . ! E
        # (4) E -> . E & E
        # (5) E -> . E | E
        # (6) E -> . E ^ E
        # (7) E -> . E ~ E
        "X": ("s", 2),  # shift and go to state 2
        "(": ("s", 3),  # shift and go to state 3
        "!": ("s", 4),  # shift and go to state 4
        "E": ("s", 13),  # shift and go to state 13
    },
    8: {  # state 8
        # (7) E -> E ~ . E
        # (1) E -> . X
        # (2) E -> . ( E )
        # (3) E -> . ! E
        # (4) E -> . E & E
        # (5) E -> . E | E
        # (6) E -> . E ^ E
        # (7) E -> . E ~ E
        "X": ("s", 2),  # shift and go to state 2
        "(": ("s", 3),  # shift and go to state 3
        "!": ("s", 4),  # shift and go to state 4
        "E": ("s", 14),  # shift and go to state 14
    },
    9: {  # state 9
        # (2) E -> ( E . )
        # (4) E -> E . & E
        # (5) E -> E . | E
        # (6) E -> E . ^ E
        # (7) E -> E . ~ E
        ")": ("s", 15),  # shift and go to state 15
        "&": ("s", 5),  # shift and go to state 5
        "|": ("s", 6),  # shift and go to state 6
        "^": ("s", 7),  # shift and go to state 7
        "~": ("s", 8),  # shift and go to state 8
    },
    10: {  # state 10
        # (3) E -> ! E .
        # (4) E -> E . & E
        # (5) E -> E . | E
        # (6) E -> E . ^ E
        # (7) E -> E . ~ E
        "&": ("r", 3),  # reduce using rule 3 (E -> ! E .)
        "|": ("r", 3),  # reduce using rule 3 (E -> ! E .)
        "^": ("r", 3),  # reduce using rule 3 (E -> ! E .)
        "~": ("r", 3),  # reduce using rule 3 (E -> ! E .)
        "$": ("r", 3),  # reduce using rule 3 (E -> ! E .)
        ")": ("r", 3),  # reduce using rule 3 (E -> ! E .)
        # ! &               [ shift and go to state 5 ]
        # ! |               [ shift and go to state 6 ]
        # ! ^               [ shift and go to state 7 ]
        # ! ~               [ shift and go to state 8 ]
    },
    11: {  # state 11
        # (4) E -> E & E .
        # (4) E -> E . & E
        # (5) E -> E . | E
        # (6) E -> E . ^ E
        # (7) E -> E . ~ E
        "&": ("r", 4),  # reduce using rule 4 (E -> E & E .)
        "|": ("r", 4),  # reduce using rule 4 (E -> E & E .)
        "^": ("r", 4),  # reduce using rule 4 (E -> E & E .)
        "~": ("r", 4),  # reduce using rule 4 (E -> E & E .)
        "$": ("r", 4),  # reduce using rule 4 (E -> E & E .)
        ")": ("r", 4),  # reduce using rule 4 (E -> E & E .)
        # ! &               [ shift and go to state 5 ]
        # ! |               [ shift and go to state 6 ]
        # ! ^               [ shift and go to state 7 ]
        # ! ~               [ shift and go to state 8 ]
    },
    12: {  # state 12
        # (5) E -> E | E .
        # (4) E -> E . & E
        # (5) E -> E . | E
        # (6) E -> E . ^ E
        # (7) E -> E . ~ E
        "|": ("r", 5),  # reduce using rule 5 (E -> E | E .)
        "^": ("r", 5),  # reduce using rule 5 (E -> E | E .)
        "~": ("r", 5),  # reduce using rule 5 (E -> E | E .)
        "$": ("r", 5),  # reduce using rule 5 (E -> E | E .)
        ")": ("r", 5),  # reduce using rule 5 (E -> E | E .)
        "&": ("s", 5),  # shift and go to state 5
        # ! &               [ reduce using rule 5 (E -> E | E .) ]
        # ! |               [ shift and go to state 6 ]
        # ! ^               [ shift and go to state 7 ]
        # ! ~               [ shift and go to state 8 ]
    },
    13: {  # state 13
        # (6) E -> E ^ E .
        # (4) E -> E . & E
        # (5) E -> E . | E
        # (6) E -> E . ^ E
        # (7) E -> E . ~ E
        "^": ("r", 6),  # reduce using rule 6 (E -> E ^ E .)
        "~": ("r", 6),  # reduce using rule 6 (E -> E ^ E .)
        "$": ("r", 6),  # reduce using rule 6 (E -> E ^ E .)
        ")": ("r", 6),  # reduce using rule 6 (E -> E ^ E .)
        "&": ("s", 5),  # shift and go to state 5
        "|": ("s", 6),  # shift and go to state 6
        # ! &               [ reduce using rule 6 (E -> E ^ E .) ]
        # ! |               [ reduce using rule 6 (E -> E ^ E .) ]
        # ! ^               [ shift and go to state 7 ]
        # ! ~               [ shift and go to state 8 ]
    },
    14: {  # state 14
        # (7) E -> E ~ E .
        # (4) E -> E . & E
        # (5) E -> E . | E
        # (6) E -> E . ^ E
        # (7) E -> E . ~ E
        "~": ("r", 7),  # reduce using rule 7 (E -> E ~ E .)
        "$": ("r", 7),  # reduce using rule 7 (E -> E ~ E .)
        ")": ("r", 7),  # reduce using rule 7 (E -> E ~ E .)
        "&": ("s", 5),  # shift and go to state 5
        "|": ("s", 6),  # shift and go to state 6
        "^": ("s", 7),  # shift and go to state 7
        # ! &               [ reduce using rule 7 (E -> E ~ E .) ]
        # ! |               [ reduce using rule 7 (E -> E ~ E .) ]
        # ! ^               [ reduce using rule 7 (E -> E ~ E .) ]
        # ! ~               [ shift and go to state 8 ]
    },
    15: {  # state 15
        # (2) E -> ( E ) .
        "&": ("r", 2),  # reduce using rule 2 (E -> ( E ) .)
        "|": ("r", 2),  # reduce using rule 2 (E -> ( E ) .)
        "^": ("r", 2),  # reduce using rule 2 (E -> ( E ) .)
        "~": ("r", 2),  # reduce using rule 2 (E -> ( E ) .)
        "$": ("r", 2),  # reduce using rule 2 (E -> ( E ) .)
        ")": ("r", 2),  # reduce using rule 2 (E -> ( E ) .)
    },
}
