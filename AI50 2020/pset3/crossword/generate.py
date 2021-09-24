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
                        w, h = draw.textsize(letters[i][j], font=font)
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
        for d in self.domains:
            for word in self.domains[d].copy():
                if not len(word) == d.length:
                    self.domains[d].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[(x, y)]
        for x_val in self.domains[x].copy():
            valid = False
            for y_val in self.domains[y]:
                if x_val[overlap[0]] == y_val[overlap[1]]:
                    valid = True
            if not valid:
                self.domains[x].remove(x_val)
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = []
        for overlap in self.crossword.overlaps:
            if self.crossword.overlaps[overlap]:
                queue.append(overlap)
        while queue:
            arc = queue.pop(0)
            if self.revise(arc[0], arc[1]):
                if not self.domains[arc[0]]:
                    return False
                for ngb in self.crossword.neighbors(arc[0]):
                    if not ngb == arc[1]:
                        queue.append((ngb, arc[0]))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.crossword.variables:
            if variable not in assignment or not assignment[variable]:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        consistent = True
        words_used = set()
        for value in assignment:
            # length
            if not len(assignment[value]) == value.length:
                consistent = False
            # unique words
            if assignment[value] in words_used:
                consistent = False
            # conflicts
            for ngb in self.crossword.neighbors(value):
                overlap = self.crossword.overlaps[(value,ngb)]
                if overlap and ngb in assignment:
                    if assignment[value][overlap[0]] != assignment[ngb][overlap[1]]:
                        consistent = False
            words_used.add(assignment[value])

        return consistent

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domain = list(self.domains[var])
        # get the set of all neighbours without assigned values
        unsigned_ngbs = set()
        for ngb in self.crossword.neighbors(var):
            if ngb not in assignment:
                unsigned_ngbs.add(ngb)
        # if all neighbours are assigned there's no point in sorting
        if len(unsigned_ngbs) > 0:
            # count how many times each possible value rules out another
            for i in range(len(domain)):
                conflicts = 0
                for ngb in unsigned_ngbs:
                    overlap = self.crossword.overlaps[(var, ngb)]
                    value_letter = domain[i][overlap[0]]
                    for ngb_val in self.domains[ngb]:
                        ngb_letter = ngb_val[overlap[1]]
                        if not ngb_letter == value_letter:
                            conflicts += 1
                domain[i] = (domain[i], conflicts)
            domain.sort(key=lambda x: x[1])
            domain = [x[0] for x in domain]
        return domain

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        sorted_vars = []
        for variable in self.crossword.variables:
            if variable in assignment:
                continue
            sorted_vars.append((variable, len(self.domains[variable]), len(self.crossword.neighbors(variable))))
        sorted_vars.sort(key=lambda x: x[2], reverse=True)  # sort by degree
        sorted_vars.sort(key=lambda x: x[1])  # sort by domain size
        sorted_vars = [x[0] for x in sorted_vars]
        return sorted_vars[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(var, assignment):
            consistency_test = assignment.copy()
            consistency_test[var] = val
            if self.consistent(consistency_test):
                assignment[var] = val
                result = self.backtrack(assignment)
                if result:
                    return result
                assignment.pop(var)
        return None


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
