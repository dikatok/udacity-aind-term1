
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]


rows = 'ABCDEFGHI'
cols = '123456789'

# list all positions in sudoku grid
boxes = cross(rows, cols)

# list every row units (from top to bottom)
row_units = [cross(r, cols) for r in rows]
# list every column units (from left to right)
column_units = [cross(rows, c) for c in cols]
# list every square units (from left to right and top to bottom)
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# list boxes in left diagonal (bottom left to upper right)
left_diag_units = [[a+b for (a, b) in list(zip(rows[::-1], cols))]]
# list boxes in right diagonal (upper left to bottom right)
right_diag_units = [[a+b for (a, b) in list(zip(rows, cols))]]
# combine all units
unitlist = row_units + column_units + square_units + left_diag_units + right_diag_units
# create mapping between each box and units they are belong to
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# create mapping between each box and their peers
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for box in values.keys():
        for box_units in units[box]:
            twins = [unit for unit in box_units if values[box] == values[unit]]
            if len(twins) > 1 and len(twins) == len(values[box]):
                for unit in box_units:
                    if unit not in twins:
                        for value in values[box]:
                            values[unit] = values[unit].replace(value, "")
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    print('\n')
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """

    # preserve the original sudoku dict by performing shallow copy
    new_grid = values.copy()

    # eliminate impossible values for each unsolved box by looking at it's "solved" peers
    for key in values.keys():
        if len(values[key]) > 1:
            possible_values = values[key]
            for peer in peers[key]:
                if len(values[peer]) == 1:
                    possible_values = possible_values.replace(values[peer], "")
            new_grid[key] = possible_values
    return new_grid


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """

    # assign the only choice for each unsolved box if exists
    for unit in unitlist:
        for box_key in unit:
            all_values = "".join(values[unit_key] for unit_key in unit if unit_key != box_key)
            for value in "123456789":
                if all_values.find(value) < 0 <= values.get(box_key).find(value):
                    values[box_key] = value
    return values


def reduce_puzzle(values):
    """Optimize/reduce the possible values of each unit.

    Perform elimination and only choice strategies until all possible values are optimized.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after optimization.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        values = naked_twins(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return values
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku recursively."
    values = reduce_puzzle(values)

    # validate every units
    for unit in unitlist:
        if (len([values[box] for box in unit if len(values[box]) == 1])
                != len(set([values[box] for box in unit if len(values[box]) == 1]))) \
                or any(len(values[box]) == 0 for box in unit):
            return False

    # check if sudoku is solved, if so then return current values which is the solution
    if all(len(values[box]) == 1 for box in values.keys()):
        return values

    # get the unsolved box with minimum possible values
    min_values, box = min((len(values[box]), box) for box in values.keys() if len(values[box]) > 1)
    # preserve the original grid values at this point
    copied = values.copy()
    # choose 1 possible box value at one time, and recursively perform search on the remaining boxes
    for value in values[box]:
        copied[box] = value
        result = search(copied)
        # return the solution (result != False)
        if result:
            return result
    return False


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # create sudoku grid representation as dictionary and replace unsolved boxes with all possible values
    grid = grid_values(grid)

    # perform DFS on grid and return the answer
    return search(grid)


if __name__ == '__main__':
    grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    solved_grid = solve(grid)
    display(solved_grid)

