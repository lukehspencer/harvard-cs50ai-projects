import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# Store all sentence structures and grammar rules that are applicable to each sentence in the `sentences` directory
NONTERMINALS = """
S -> NP VP 
S -> NP VP PP 
S -> NP VP PP CP VP 
S -> NP VP ADJP 
S -> ADVP VP NP CP VP PP
S -> NP ADVP CP NP 
S -> NP VP ADJP PP CP PP 
S -> NP VP ADJP NP PP PP
S -> NP PP

NP -> Det N | N
VP -> V | V NP
ADJP -> Adj | Adj NP | Det Adj NP | Det Adj Adj Adj 
PP -> P | P NP | P ADJP | P NP Adv
CP -> Conj NP | Conj VP
ADVP -> NP Adv | VP Adv
""" 

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Splits every word in sentence and stores it in a list
    word_list = nltk.word_tokenize(sentence.lower())

    # Iterates through every word in the sentence and remove any that don't contain at least one alphabetical character
    for word in word_list:
        length = 0
        for char in word:
            if not char.isalpha():
                length+=1
        
        if length == len(word):
            word_list.remove(word)
    
    return word_list
    raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Stores every noun phrase (NP) in tree into nps
    nps = []
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            nps.append(subtree)
    
    # Iterate through all NPs in tree and adds any that don't contain any other NPs
    np_chunks = []
    for tree in nps:
        contained = False
        for other_tree in nps:
            if tree == other_tree:
                continue
            if other_tree in tree.subtrees():
                contained = True
                break

        if not contained:
            np_chunks.append(tree)

    return np_chunks
    raise NotImplementedError


if __name__ == "__main__":
    main()

