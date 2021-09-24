from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Not(And(AKnight, AKnave)),  # but he can't be both
    Biconditional(And(AKnight, AKnave), AKnight), # if what A says is true, they're a knight
    Biconditional(Not(And(AKnight, AKnave)), AKnave)  # if what A says is a lie, that implies they're a knave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Not(And(AKnight, AKnave)),  # but he can't be both

    Or(BKnight, BKnave),  # B is either a knight or a knave
    Not(And(BKnight, BKnave)),  # but he can't be both

    # if what A says is false, that implies they're a knave
    # if A is a knave, what he says is false
    Biconditional((And(AKnave, BKnave)), AKnight),
    Biconditional(Not(And(AKnave, BKnave)), AKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Not(And(AKnight, AKnave)),  # but he can't be both

    Or(BKnight, BKnave),  # B is either a knight or a knave
    Not(And(BKnight, BKnave)),  # but he can't be both
    # what A says
    Biconditional(Or(And(AKnight, BKnight), And(AKnave, BKnave)),AKnight),
    # what B says
    Biconditional(And(Not(And(AKnight, BKnight)), Not(And(AKnave, BKnave))),BKnight),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave
    Not(And(AKnight, AKnave)),  # but he can't be both

    Or(BKnight, BKnave),  # B is either a knight or a knave
    Not(And(BKnight, BKnave)),  # but he can't be both

    Or(CKnight, CKnave),  # C is either a knight or a knave
    Not(And(CKnight, CKnave)),  # but he can't be both

    # what A says
    Or(Biconditional(AKnight, AKnight),
       Biconditional(AKnave, AKnight)),
    # what B says
    Biconditional(Biconditional(AKnave, AKnight), BKnight),
    Biconditional(CKnave, BKnight),
    # what C says
    Biconditional(AKnight, CKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
