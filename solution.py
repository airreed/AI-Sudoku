assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        
        for unit in unitlist:
            # Find naked twins for this unit
            twins1, twins2 = find_twins(values, unit)
            if twins1 == "":
                continue
#            print("Twins are: ", twins1, twins2)
#            print("In unit: ", unit)
#            print("Letters are: ", values[twins1])
            for box in unit:
                if box == twins1 or box == twins2:
                    continue
                for l in values[twins1]:
                    assign_value(values, box, values[box].replace(l, ""))
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
      
    return values
    
def find_twins(values, unit):
    """Find twins in the current unit.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        unit: a column, a row, a square or a diagonal

    Returns:
        the twins with same two letters.
        two empty if no twins found
    """
    twos = []
    for box in unit:
        if len(values[box]) == 2:
            for t in twos:
                if values[box] == values[t]:
                    return box, t
            twos.append(box)
    return "", ""
                        
        

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

diagonal_units = [['A1','B2','C3','D4','E5','F6','G7','H8','I9'],
                  ['A9','B8','C7','D6','E5','F4','G3','H2','I1']]
unitlist_diagonal = unitlist + diagonal_units
units_diagonal = dict((s, [u for u in unitlist_diagonal if s in u]) for s in boxes)
peers_diagonal = dict((s, set(sum(units_diagonal[s],[]))-set([s])) for s in boxes)

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
    i = 0
    dic = {}
    for l in boxes:
        if (grid[i] == '.'):
            dic[l] = '123456789'
        else:
            dic[l] = grid[i]
        i += 1
    return dic

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for key, value in values.items():
        if len(value) == 1:
            for peer in peers_diagonal[key]:
                assign_value(values, peer, values[peer].replace(value, ""))
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist_diagonal:
        for digit in '123456789':
            hasBox = []
            for box in unit:
                if digit in values[box]:
                    hasBox.append(box)
            if len(hasBox) == 1:
                assign_value(values, hasBox[0], digit)
    return values

def naked_twins_diagonal(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers   
    for unit in unitlist_diagonal:
        twins1, twins2 = find_twins(values, unit)
        if twins1 == "":
            continue
        for box in unit:
            if box == twins1 or box == twins2:
                continue
            for l in values[twins1]:
                assign_value(values, box, values[box].replace(l, ""))
    return values

def hidden_twins_diagonal(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist_diagonal:
        # for each digit, record in which boxes it appears, as a string of the boxes conbined
        digitbox = [''] * 10
        for box in unit:
            for digit in values[box]:
                digitbox[int(digit)] = digitbox[int(digit)] + box
#        print("digitbox::::::", digitbox)
        for i in range(2,10):
            for j in range(1,i):
                if len(digitbox[i]) == 4 and digitbox[i] == digitbox[j]:
#                    print("found!!!!!!!!!!!!!!!!!", digitbox[i][0:2], digitbox[i][2:4])
                    twin = str(j) + str(i)
                    # assign the two digits as the only candidates
                    values[digitbox[i][0:2]] = twin
                    values[digitbox[i][2:4]] = twin
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        eliminate(values)
        
        only_choice(values)
        
        hidden_twins_diagonal(values)
        
        naked_twins_diagonal(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    """
    import copy
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values) 
    if values == False:
        return False
    # Choose one of the unfilled squares with the fewest possibilities
    n = 9
    smallBox = ""
    for box in boxes:
        if len(values[box]) != 1 and len(values[box]) < n:
            n = len(values[box])
            smallBox = box
    if smallBox == '':
        return values
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    origin = values[smallBox]
    for i in origin:
        board = copy.deepcopy(values)
        board[smallBox] = i
        board = search(board) # necessary
        if board:
            return board
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
    values = grid_values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
