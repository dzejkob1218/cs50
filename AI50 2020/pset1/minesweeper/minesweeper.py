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
        # if there are as many cells as count, all of them are mines
        if len(self.cells) == self.count:
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if count is 0 then there are no mines and all cells are safe
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


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
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Make a new sentence from the last move
        new_cells = []
        nearby = nearby_cells(cell, self.height, self.width)
        for n in nearby:
            if n not in self.safes and n not in self.moves_made:
                new_cells.append(n)
        self.new_sentence(new_cells, count)

        # Let all sentences check themselves for new information
        # Loop until no new conclusions are made
        done = False
        while not done:
            done = True
            for sent in self.knowledge.copy():
                new_safes = sent.known_safes()
                new_mines = sent.known_mines()
                if new_mines or new_safes:
                    done = False
                    self.knowledge.remove(sent)
                    if new_mines:
                        for mine in new_mines.copy():
                            self.mark_mine(mine)
                    if new_safes:
                        for safe in new_safes.copy():
                            self.mark_safe(safe)

            # Go through all the sentences to see if some include others
            for top_sent in self.knowledge.copy():
                for bot_sent in self.knowledge.copy():
                    if len(bot_sent.cells) < 2 or len(top_sent.cells) < 2:
                        continue
                    if bot_sent == top_sent:
                        continue
                    if bot_sent.cells.issubset(top_sent.cells):
                        diff_cells = top_sent.cells - bot_sent.cells
                        diff_count = top_sent.count - bot_sent.count
                        print(f"Making conclusions; {bot_sent.cells} is subset of {top_sent.cells}")
                        done = False
                        if top_sent in self.knowledge:
                            self.knowledge.remove(top_sent)
                        self.new_sentence(diff_cells, diff_count)

        self.knowledge_cleanup()

    def new_sentence(self, cells, count):
        new_sent = Sentence(cells, count)
        # Before a new sentence is added, it has to go through updating all safes and mines it 'missed out' on
        for safe in self.safes:
            new_sent.mark_safe(safe)
        for mine in self.mines:
            new_sent.mark_mine(mine)
        if new_sent.cells:
            self.knowledge.append(new_sent)

    def knowledge_cleanup(self):
        """ Removes empty sentences that sometimes accumulate """
        clean_knowledge = []
        for sent in self.knowledge:
            if len(sent.cells) < 1:
                continue
            clean_knowledge.append(sent)
        self.knowledge = clean_knowledge

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines:
                return i, j

def nearby_cells(cell, height, width):
    cells = []
    # Loop over all cells within one row and column
    for i in range(cell[0] - 1, cell[0] + 2):
        for j in range(cell[1] - 1, cell[1] + 2):

            # Ignore the cell itself
            if (i, j) == cell:
                continue

            # Update count if cell in bounds and is mine
            if 0 <= i < height and 0 <= j < width:
                cells.append((i,j))

    return cells
