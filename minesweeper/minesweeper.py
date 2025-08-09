import itertools
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If the number of cells is equal to the number of mines, then all cells are mines
        if len(self.cells) == self.count:
            return self.cells

        return set()
    
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If there is 0 mines around the cells, then all cells are safe
        if self.count == 0:
            return self.cells
        
        return set()
        
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Removes the cell since it is now known to be a mine, which in turn decreases the number of mines in the sentence
        if cell in self.cells:
            self.cells.remove(cell)
            self.count-=1

        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Removes the cell since it is now known to be safe
        if cell in self.cells:
            self.cells.remove(cell)

        #raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell) # marks the cell as a move that has been made
        self.mark_safe(cell) # marks the cell as safe
        
        cells = set()
        row, col = cell
        
        # Add all surrounding cells to the set of cells if they aren't known to be moves made, mines, or safes
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i == 0 and j == 0:
                    continue
                new_cell = (row+i,col+j)
                if 0 <= row+i < self.height and 0 <= col+j < self.width:
                    if new_cell not in self.moves_made and new_cell not in self.mines and new_cell not in self.safes:
                        cells.add(new_cell)
                    elif new_cell in self.mines: # if the AI finds that one of the cells is a mine, then it decreases the count of mines in the sentence
                        count-=1

        # Adds a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        new_sentence = Sentence(cells,count)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

        # Iteratively marks any additional cells as safe or as mines and infers new sentences
        changed = True # used to track if any changes were made to the knowledge base (if none then the loop can be exited)
        while changed:
            changed = False
            removed = []
            added = []
            
            # Marks any additional cells as safe or as mines
            for sentence in self.knowledge:
                if sentence.known_mines():
                    for mine in sentence.known_mines().copy():
                        self.mark_mine(mine)
                        changed = True
                if sentence.known_safes():
                    for safe in sentence.known_safes().copy():
                        self.mark_safe(safe)
                        changed = True
                if len(sentence.cells) == 0 and sentence not in removed:
                    removed.append(sentence)
                    changed = True

            # Infers new sentences if sentence1 is a subset of sentence2 (then new sentence can be inferred and added to KB)
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1 is sentence2:
                        continue
                    if sentence1 == sentence2:
                        self.knowledge.remove(sentence2)
                    if sentence1 in removed or sentence2 in removed:
                        continue
                    if sentence1.cells.issubset(sentence2.cells): 
                        subset_count = sentence2.count - sentence1.count
                        subset_cells = sentence2.cells - sentence1.cells
                        new_sentence = Sentence(subset_cells, subset_count)
                        if new_sentence not in self.knowledge:
                            added.append(new_sentence)
                            changed = True

            # Updates KB by removing any sentences that are empty           
            for sentence in removed:
                if sentence in self.knowledge.copy():
                    self.knowledge.remove(sentence)

            # Updates KB by adding any new sentences that were inferred
            for sentence in added:
                self.knowledge.append(sentence)

        #raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Iterates through all safe cells and checks to see if they have already been made
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        
        return None

        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # If all cells have been explored or are mines, return None
        if len(self.moves_made) + len(self.mines) == self.height * self.width:
            return None

        # Chooses a random position on the board that has not been made yet and is not a mine
        while True:
            cell = random.choice(list(itertools.product(list(range(self.width)), list(range(self.height)))))
            if cell not in self.moves_made and cell not in self.mines:
                self.moves_made.add(cell)
                return cell
    
        raise NotImplementedError
