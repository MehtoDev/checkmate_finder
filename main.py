import copy
from operator import add

def is_valid_position(col, row):
    return 0 <= col < 8 and 0 <= row < 8

def square_empty(col, row, board):
    return board[col][row] == '.'

def get_king_moves(col, row, board):
    moves = []
    king_moves = [[0,-1],[0,1],[1,0],[-1,0],[1,-1],[-1,-1],[1,1],[-1,1]]
    for move in king_moves:
        new_col, new_row = map(add, [col,row], move)
        if is_valid_position(new_col, new_row):
            if square_empty(new_col, new_row, board) or (board[new_col][new_row].islower() != board[col][row].islower()):
                moves.append([(col, row), (new_col, new_row)])
    return moves

def get_pawn_moves(col, row, board):
    moves = []

    color_mult = 1 if board[col][row].isupper() else -1
    has_moved = False if (color_mult > 0 and row == 1) or (color_mult < 0 and row == 6) else True

    pawn_moves = []
    if not has_moved:
        pawn_moves = [[0,2],[0,1],[1,1],[-1,1]]
    else:
        pawn_moves = [[0,1],[1,1],[-1,1]]

    for move in pawn_moves:
        move = [color_mult * x for x in move]
        new_col, new_row = map(add, [col,row], move)
        if is_valid_position(new_col, new_row):
            if move[0] == 0 and square_empty(new_col,new_row, board):
                if new_row == (7 if color_mult > 0 else 0):
                    moves.append([(col, row), (new_col, new_row), 'Q'])
                    moves.append([(col, row), (new_col, new_row), 'R'])
                    moves.append([(col, row), (new_col, new_row), 'B'])
                    moves.append([(col, row), (new_col, new_row), 'N'])
                else:
                    moves.append([(col, row), (new_col, new_row)])
            if move[0] != 0 and (not square_empty(new_col,new_row, board)):
                piece, empty = get_piece(new_col, new_row, board)
                if not empty and (piece.isupper() and color_mult < 0) or (piece.islower() and color_mult > 0):
                    if new_row == (7 if color_mult > 0 else 0):
                        moves.append([(col, row), (new_col, new_row), 'Q'])
                        moves.append([(col, row), (new_col, new_row), 'R'])
                        moves.append([(col, row), (new_col, new_row), 'B'])
                        moves.append([(col, row), (new_col, new_row), 'N'])
                    else:
                        moves.append([(col, row), (new_col, new_row)])
    return moves

def get_knight_moves(col, row, board):
    moves = []
    knight_moves = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[1,-2],[-1,2],[-1,-2]]

    for move in knight_moves:
        new_col, new_row = map(add, [col,row], move)
        if is_valid_position(new_col, new_row):
            if board[new_col][new_row] == '.' or (board[new_col][new_row].islower() != board[col][row].islower()):
                moves.append([(col, row), (new_col, new_row)])
    return moves

def get_rook_moves(col, row, board):
    moves = []
    directions = [[0,-1],[0,1],[1,0],[-1,0]]

    for direction in directions:
        new_col, new_row = map(add, [col, row], direction)
        while is_valid_position(new_col,new_row) and square_empty(new_col,new_row,board):
            moves.append([(col,row),(new_col,new_row)])
            new_col, new_row = map(add, [new_col,new_row], direction)
        if is_valid_position(new_col,new_row):
            target_piece = board[new_col][new_row]
            piece = board[col][row]
            if target_piece.isupper() != piece.isupper():
                moves.append([(col,row),(new_col,new_row)])
    return moves

def get_bishop_moves(col, row, board):
    moves = []
    directions = [[1,-1],[-1,-1],[1,1],[-1,1]]

    for direction in directions:
        new_col, new_row = map(add, [col, row], direction)
        while is_valid_position(new_col,new_row) and square_empty(new_col,new_row,board):
            moves.append([(col,row),(new_col,new_row)])
            new_col, new_row = map(add, [new_col,new_row], direction)
        if is_valid_position(new_col,new_row):
            target_piece = board[new_col][new_row]
            piece = board[col][row]
            if target_piece.isupper() != piece.isupper():
                moves.append([(col,row),(new_col,new_row)])
    return moves

def get_queen_moves(col, row, board):
    moves = []
    moves.extend(get_rook_moves(col, row, board))
    moves.extend(get_bishop_moves(col, row, board))
    return moves

def get_moves(col, row, board):
    piece, empty = get_piece(col, row, board)
    if empty:
        return []
    
    switch_dict = {
        'Q': get_queen_moves,
        'K': get_king_moves,
        'N': get_knight_moves,
        'P': get_pawn_moves,
        'R': get_rook_moves,
        'B': get_bishop_moves,
        'q': get_queen_moves,
        'k': get_king_moves,
        'n': get_knight_moves,
        'p': get_pawn_moves,
        'r': get_rook_moves,
        'b': get_bishop_moves,
    }
    moves = switch_dict[piece](col, row, board)
    return moves

def get_legal_moves(col, row, board):
    moves = get_moves(col, row, board)
    color = 'white' if board[col][row].isupper() else 'black'
    legal_moves = []

    for move in moves:
        new_board = make_move(move,copy.deepcopy(board))
        checked_after = is_in_check(color, new_board)
        if not checked_after:
            legal_moves.append(move)
    return legal_moves

def is_in_check(color, board):
    for i in range(8):
        for j in range(8):
            piece, _ = get_piece(i, j, board)
            if piece.lower() == 'k' and (color == 'white' and piece.isupper() or color == 'black' and piece.islower()):
                friendly_king_pos = (i, j)
            if piece.lower() == 'k' and (color == 'black' and piece.isupper() or color == 'white' and piece.islower()):
                opposing_king_pos = (i, j)
    
    for i in range(8):
        for j in range(8):
            piece, _ = get_piece(i, j, board)
            if piece.lower() != 'k' and (color == 'white' and piece.islower() or color == 'black' and piece.isupper()):
                _moves = get_moves(i, j, board)
                _moves.extend(get_king_moves(*opposing_king_pos, board))
                moves = [move[1] for move in _moves]
                if friendly_king_pos in moves:
                    return True
    return False

def make_move(move, board):
    if len(move) == 2:
        col,row = move[0]
        new_col, new_row = move[1]
        new_board = board
        new_board[new_col][new_row] = new_board[col][row]
        new_board[col][row] = '.'
    if len(move) == 3:
        col,row = move[0]
        new_col, new_row = move[1]
        new_board = board
        new_board[new_col][new_row] = move[2]
        new_board[col][row] = '.'
    return new_board

def is_checkmate(color, board):
    legal_moves = all_legal_moves(color, board)
    checked = is_in_check(color, board)
    if legal_moves or not checked:
        return False
    return True

def all_legal_moves(color, board):
    legal_moves = []
    for col in range(8):
        for row in range(8):
            piece, empty = get_piece(col, row, board)
            if not empty and (color == 'white' and piece.isupper() or color == 'black' and piece.islower()):
                moves = get_legal_moves(col, row, board)
                legal_moves.extend(moves)
    return legal_moves

def get_coordinate(col, row):
    letters = ['a','b','c','d','e','f','g','h']
    return f'{letters[col]}{row+1}'

def get_index(s):
    letters = ['a','b','c','d','e','f','g','h']
    return  letters.index(s[0]), int(s[1])-1

def get_piece(col, row, board):
    return board[col][row], square_empty(col, row, board)


if __name__ == "__main__":
    board = [['.' for _ in range(8)] for _ in range(8)]
    for i in range(8):
        row_input = input().strip()
        row_input = list(row_input)
        for j in range(len(row_input)):
            board[j][-i-1] = row_input[j]

    moves = all_legal_moves('white', board)
    for move in moves:
        new_board = copy.deepcopy(board)
        new_board = make_move(move, new_board)
        mate = is_checkmate('black', new_board)
        if mate:
            print(f'{get_coordinate(*move[0])}{get_coordinate(*move[1])}')