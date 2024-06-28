from models.tictactoe.constants import CELL_EMPTY, PLAYER_1, PLAYER_2
from models.tictactoe.constants import COLS_N, ROWS_N
from models.tictactoe.constants import STATE_CONTINUE, STATE_DRAW
from models.tictactoe.constants import REQUIRED_LINE


class Cell():
    def __init__(self, color):
        self.color = color
        self.marked = False

class Board():
    def __init__(self):
        self.cells = [list(Cell(CELL_EMPTY) for _ in range(COLS_N)) for _ in range(ROWS_N)]
    
    def get_cell(self, col, row):
        if ((row >= 0 and row < ROWS_N) and (col >= 0 and col < COLS_N)):
            return self.cells[col][row]
        return None
    
    def load_cells(self, cells):
        self.cells = cells

    def has_spaces(self):
        for row in self.cells:
            for cell in row:
                if cell.color == CELL_EMPTY:
                    return True
        return False
    
    def has_marked_cells(self):
        for row in self.cells:
            for cell in row:
                if cell.marked:
                    return True
        return False
    
    def print_board(self):
        for col in range(COLS_N):
            for row in range(ROWS_N):
                cell = self.get_cell(col, row)
                if cell != None:
                    cell: Cell
                    print(f'|{cell.color}|', end="")
                else:
                    print('| |', end="")
            print("")
        print("")

class TicTacToe():
    def __init__(self, start_turn = PLAYER_1):
        self.turn = start_turn
        self.new_game()

    def new_game(self):
        self.board = Board()
        self.state = STATE_CONTINUE

    def load_game(self, board, state, turn):
        self.board = board
        self.state = state
        self.turn = turn

    def next_turn(self):
        self.turn = PLAYER_2 if self.turn == PLAYER_1 else PLAYER_1

    def check_win(self, c: Cell, col, row):
        lst_vertical = [c]
        lst_horizontal = [c]
        lst_diagonal_a = [c]
        lst_diagonal_b = [c]
        # add recursively, starting from p, aligned pieces that are of the same color
        for n in [1, -1]:
            self.add_to_lst_recursive(c.color, col, row, n, 0, lst_vertical)
            self.add_to_lst_recursive(c.color, col, row, 0, n, lst_horizontal)  
            self.add_to_lst_recursive(c.color, col, row, n, n, lst_diagonal_a)
            self.add_to_lst_recursive(c.color, col, row, n * -1, n, lst_diagonal_b)
        # set marks if the minimum required number for a line is met
        for lst in [lst_vertical, lst_horizontal, lst_diagonal_a, lst_diagonal_b]:
            if len(lst) >= REQUIRED_LINE:
                self.set_marks(lst)

    # helper for check_win
    def add_to_lst_recursive(self, color, prev_col, prev_row, add_col, add_row, lst: list):
        c = self.board.get_cell(prev_col + add_col, prev_row + add_row)
        if c != None:
            c: Cell
            if c.color == color:
                lst.append(c)
                self.add_to_lst_recursive(color, prev_col + add_col, prev_row + add_row, add_col, add_row, lst)

    def set_marks(self, lst):
        for cell in lst:
            cell: Cell
            cell.marked = True

    def make_move(self, col, row):
        if self.state == STATE_CONTINUE:
            if ((row >= 0 and row < ROWS_N) and (col >= 0 and col < COLS_N)):
                cell: Cell = self.board.get_cell(col, row)
                if cell.color == CELL_EMPTY:
                    cell.color = self.turn
                    self.check_win(cell, col, row)
                    self.update_state()
                    self.next_turn()
                    return True
        return False
    
    def update_state(self):
        if self.board.has_marked_cells():
            self.state = self.turn
        else:
            if not self.board.has_spaces():
                self.state = STATE_DRAW

    def print_game(self):
        self.board.print_board()
        print("TURN: ", self.turn)
        print("STATE: ", self.state)

