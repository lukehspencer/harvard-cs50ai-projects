import sys

from crossword import *

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self): 
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Removes word from a variable if it isn't equal to the length
        for variable in self.crossword.variables: # go through all variables
            for word in self.domains[variable].copy(): # go through all the words in each variable's domain
                if len(word) != variable.length: # checks if the length of the word is not equal to the length of the variable's boxes
                    self.domains[variable].remove(word) # removes that word from domain 

        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        if self.crossword.overlaps[x,y] is not None:
            i, j = self.crossword.overlaps[x,y]
            for x_word in self.domains[x].copy(): # for every word in x's domain
                found = False
                for y_word in self.domains[y]: # for every word in y'd domain
                    # if the ith character of x's word equals jth character of y's word, then move on to the next word in x's domain
                    if x_word[i] == y_word[j]:
                        found = True
                        break
                
                # If the word in x's domain isn't equal to any of y's words in its domain, then remove it from x's domain
                if not found:
                    self.domains[x].remove(x_word)
                    revised = True

        return revised
        
        # raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Initializes arcs to be every arc in the problem if arcs is none
        if arcs is None:
            arcs = []
            seen = set()
            for x_var in self.crossword.variables:
                for y_var in self.crossword.neighbors(x_var):
                    if (x_var, y_var) not in seen and (y_var, x_var) not in seen:
                        arcs.append((x_var, y_var))
                        seen.add((x_var, y_var))
        
        # Iterates through all arcs
        while arcs:
            (x, y) = arcs.pop(0) # remove the first arc
            if self.revise(x, y): # makes x arc consistent with y
                if len(self.domains[x]) == 0: # if there is no more words in x's domain, then there is no solution to the problem
                    return False
                
                # Adds every variable z (besides y) to arcs as another arc (z, x) 
                for z in self.crossword.neighbors(x) - {y}: 
                    arcs.append((z,x))
        
        return True

        raise NotImplementedError

    def assignment_complete(self, assignment): 
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Checks to see if every variable in crossword problem is assigned
        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                return False
             
        return True
        
        raise NotImplementedError

    def consistent(self, assignment): 
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Checks the length of the word is not equal to length of the variable
        for variable in assignment.keys():
            if len(assignment[variable]) != variable.length:
                return False

        # Checks to see if there are any duplicate words in assignment and checks to see if there is any neighbor conflicts
        for variable1 in assignment.keys():    
            for variable2 in assignment.keys():
                if assignment[variable1] is assignment[variable2]:
                    continue
                if assignment[variable1] == assignment[variable2]:
                    return False
                if self.crossword.overlaps[variable1, variable2] is not None: # checks to see if ith character from variable1's word is equal to the jth character from variable2's word
                    i, j = self.crossword.overlaps[variable1, variable2]
                    if assignment[variable1][i] != assignment[variable2][j]:
                        return False

        return True
    
        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        n_list = []
        for word1 in self.domains[var]:
            n = 0
            assignment[var] = word1 # assigns word from var's domain to var
            
            # Checks to see if any word in var's neighbors equals the word assigned to var 
            for variable in self.crossword.neighbors(var): 
                if self.crossword.overlaps[var, variable] is None:
                    continue
                for word2 in self.domains[variable]:
                    if word2 == word1:
                        n+=1
            
            n_list.append((word1, n)) # append word1 and n to list
            assignment.pop(var, word1) # remove word from var and start new assignment
        
        n_list.sort(key=lambda x: x[1]) # sort list by the smallest value of n in n_list
        val_list = [pair[0] for pair in n_list] # make a new list that only contains the word
        
        val_list.reverse() # reverse values so its in ascending order
        return val_list
        
        raise NotImplementedError

    def select_unassigned_variable(self, assignment): 
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        min_val = min(len(self.domains[v]) for v in self.crossword.variables if v not in assignment) # finds the minimum number of remaining values for every variable v not in assignment
        val_list = [v for v in self.crossword.variables if v not in assignment and len(self.domains[v]) == min_val] # adds every variable if it equals the minimum length
        
        # If there is only one element in the list, then return it (since it has the minimum number of remaining values)
        if len(val_list) == 1:
            return val_list[0]
        
        max_degree = max(len(self.crossword.neighbors(v)) for v in val_list) # finds the mximum number of degrees of remaining values for every variable v not in assignment
        degree_list = [v for v in val_list if len(self.crossword.neighbors(v)) == max_degree] # adds every variable from val_list if it equals the mximum number of degrees
        
        return degree_list[0] 

        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If every variable has been assigned, then return assignment
        if self.assignment_complete(assignment):
            return assignment 
        
        var = self.select_unassigned_variable(assignment) # select an unassigned variable
        for word in self.order_domain_values(var, assignment): # iterate through all words in var's domain based off of the criteria of order_domain_values
            assignment[var] = word # assign a word to var
            if self.consistent(assignment): # checks if assignment is still consistent
                result = self.backtrack(assignment) # backtracks assignment
                if result is not None: # if backtrack returns not none, then return backtrack value
                    return result
                assignment.pop(var, word) # remove word from var in assignment

        return None
    
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
