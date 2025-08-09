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
    Or(AKnight, AKnave), # A is either a knight or a knave
    Not(And(AKnight, AKnave)), # A cannot be both a knight and a knave

    Implication(AKnight, And(AKnight, AKnave)), # If A is a knight, then A is both a knight and a knave
    Implication(AKnave, Not(And(AKnight, AKnave))), # If A is a knave, then A is not both a knight and a knave
)

#print(knowledge0.formula())

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave), # A is either a knight or a knave
    Not(And(AKnight, AKnave)), # A cannot be both a knight and a knave

    Or(BKnight, BKnave), # B is either a knight or a knave
    Not(And(BKnight, BKnave)), # B cannot be both a knight and a knave

    Implication(AKnight, And(AKnave, BKnave)), # If A is a knight, then both A and B are knaves
    Implication(AKnave, Not(And(AKnave, BKnave))) # If A is a knave, then it is not the case that both A and B are knaves
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave), # A is either a knight or a knave
    Not(And(AKnight, AKnave)), # A cannot be both a knight and a knave

    Or(BKnight, BKnave), # B is either a knight or a knave
    Not(And(BKnight, BKnave)), # B cannot be both a knight and a knave

    Implication(AKnight, BKnight), # If A is a knight, then B is a knight
    Implication(AKnave, BKnight), # If A is a knave, then B is a knight
    Implication(BKnight, AKnave), # If B is a knight, then A is a knave
    Implication(BKnave, AKnave) # If B is a knave, then A is a knave
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave), # A is either a knight or a knave
    Not(And(AKnight, AKnave)), # A cannot be both a knight and a knave

    Or(BKnight, BKnave), # B is either a knight or a knave
    Not(And(BKnight, BKnave)), # B cannot be both a knight and a knave

    Or(CKnight, CKnave), # C is either a knight or a knave
    Not(And(CKnight, CKnave)), # C cannot be both a knight and a knave

    Implication(AKnight, Or(AKnight, AKnave)), # If A is a knight, then A is either a knight or a knave
    Implication(AKnave, Not(Or(AKnave, AKnight))), # If A is a knave, then it is not the case that A is a knave or a knight
    Implication(AKnave, BKnight), # If A is a knave, then B is a knight
    Implication(AKnight, BKnave), # If A is a knight, then B is a knave
    Implication(BKnave, CKnight), # If B is a knave, then C is a knight
    Implication(BKnight, CKnave), # If B is a knight, then C is a knave
    Implication(CKnave, AKnave), # If C is a knave, then A is a knave
    Implication(CKnight, AKnight) # If C is a knight, then A is a knight
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
        #print(knowledge.formula())
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")
    

if __name__ == "__main__":
    main()
