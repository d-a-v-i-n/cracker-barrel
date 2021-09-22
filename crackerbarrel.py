def print_board(encoding):
    '''
    This function prints an ASCII representation of the game board.

    Parameters:
        encoding - A string of 1s and 0s, which is a binary representation of
                   where the pegs are located on the board.

    Returns: None
    '''
    print(f'    {encoding[0]}')
    print(f'   {encoding[1]} {encoding[2]}')
    print(f'  {encoding[3]} {encoding[4]} {encoding[5]}')
    print(f' {encoding[6]} {encoding[7]} {encoding[8]} {encoding[9]}')
    print(f'{encoding[10]} {encoding[11]} {encoding[12]} {encoding[13]}' +
          f' {encoding[14]}')

def get_all_conceivable_moves():
    '''
    This function finds all moves that can conceivably be done, not taking
    into account specific situations.

    Parameters: None

    Returns:
        moves_both_ways - An array of tuples, where each tuple represents
                          a possible move.
    '''
    moves = set()
    moves.add((0, 1, 3))
    moves.add((0, 2, 5))
    moves.add((1, 3, 6))
    moves.add((1, 4, 8))
    moves.add((2, 4, 7))
    moves.add((2, 5, 9))
    for i in range(3, 6):
        moves.add((i, i + 3, i + 7))
        moves.add((i, i + 4, i + 9))
    moves.add((3, 4, 5))
    moves.add((6, 7, 8))
    moves.add((7, 8, 9))
    for i in range(10, 13):
        moves.add((i, i + 1, i + 2))
    moves_both_ways = set()
    for move in moves:
        moves_both_ways.add(move)
        moves_both_ways.add((move[2], move[1], move[0]))
    return moves_both_ways

def get_moves(encoding):
    '''
    This function finds what moves are possible given the current state of
    the game board.

    Parameters:
        encoding - A string of 1s and 0s, which is a binary representation of
                   where the pegs are located on the board.

    Returns:
        possible_moves - An array of tuples, where each tuple represents
                         a possible move.
    '''
    all_moves = get_all_conceivable_moves()
    possible_moves = set()
    for move in all_moves:
        if encoding[move[0]] == '1':
            if encoding[move[1]] == '1':
                if encoding[move[2]] == '0':
                    possible_moves.add(move)
    return possible_moves

def cb_one(encoding):
    '''
    This function finds one possible solution to a puzzle.

    Parameters:
        encoding - A string of 1s and 0s, which is a binary representation of
                   where the pegs are located on the board.

    Returns:
        This function returns an array of tuples, where each tuple is a move.
        If the moves are performed in order the puzzle will
        be solved (only one peg left).
    '''
    checker = []
    return(find_one_recursive(encoding, checker))

def find_one_recursive(encoding, checker, path=[]):
    '''
    This function is a helper to cb_one(), performs the actual recursion.

    Parameters:
        encoding - A string of 1s and 0s, which is a binary representation of
                   where the pegs are located on the board.

        checker -  An array that starts as empty, but is appended to if a
                   solution is found.

        path - An array that is appended to as possible moves are explored.

    Returns:
        The array showing the proper path, or None if there are no solutions.
    '''
    solved = is_solved(encoding)
    if solved:
        checker.append('FOUND')
        return path
    possible_moves = get_moves(encoding)
    if len(possible_moves) == 0:
        return
    for move in possible_moves:
        path.append(move)
        if move[2] > move[0]:
            new_encoding = (encoding[:move[0]] + '0' + encoding[move[0] +
                            1:move[1]] + '0' + encoding[move[1] + 1:move[2]] +
                            '1' + encoding[move[2] + 1:])
        else:
            new_encoding = (encoding[:move[2]] + '1' + encoding[move[2] +
                            1:move[1]] + '0' + encoding[move[1] + 1:move[0]] +
                            '0' + encoding[move[0] + 1:])
        solution = find_one_recursive(new_encoding, checker, path)
        if len(checker) != 0:
            break
        path.pop()
    return solution

def cb_all(encoding):
    '''
    This function finds all possible solutions to a puzzle.

    Parameters:
        encoding - A string of 1s and 0s, which is a binary representation of
                   where the pegs are located on the board.

    Returns:
        This function returns a 2D array, where each internal array is an
        array of tuples, where each tuple is a move. If the moves are
        performed in order the puzzle will be solved (only one peg left).
    '''
    solutions = []
    find_all_recursive(encoding, solutions)
    if solutions == []:
        return None
    return solutions

def find_all_recursive(encoding, solutions, path=[]):
    '''
    This function is a helper to cb_all(), performs the actual recursion.

    Parameters:
        encoding - A string of 1s and 0s, which is a binary representation of
                   where the pegs are located on the board.

        solutions -  An array that starts as empty, but is appended to as new
                     solutions are found.

        path - An array that is appended to as possible moves are explored.

    Returns:
        The array showing the proper path, or None if there are no solutions.
    '''
    solved = is_solved(encoding)
    if solved:
        copy = []
        for i in path:
            copy.append(i)
        solutions.append(copy)
    possible_moves = get_moves(encoding)
    if len(possible_moves) == 0:
        return
    for move in possible_moves:
        path.append(move)
        if move[2] > move[0]:
            new_encoding = (encoding[:move[0]] + '0' + encoding[move[0] +
                            1:move[1]] + '0' + encoding[move[1] + 1:move[2]] +
                            '1' + encoding[move[2] + 1:])
        else:
            new_encoding = (encoding[:move[2]] + '1' + encoding[move[2] +
                            1:move[1]] + '0' + encoding[move[1] + 1:move[0]] +
                            '0' + encoding[move[0] + 1:])
        find_all_recursive(new_encoding, solutions, path)
        path.pop()

def is_solved(encoding):
    '''
    This function is a helper to cb_one() and cb_all(). It checks to see if
    the puzzle has been solved.

    Parameters:
        encoding - A string of 1s and 0s, which is a binary representation of
                   where the pegs are located on the board.

    Returns:
        True if the puzzle has been solved, False if not.
    '''
    count = 0
    for i in encoding:
        if i == '1':
            count += 1
    if count == 1:
        return True
    return False
