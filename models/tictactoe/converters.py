from models.tictactoe.model import TicTacToe, Board, Cell
from models.tictactoe.constants import ROWS_N, COLS_N, CELL_EMPTY
import json

# game content are for storing the model in the database as json
# game is the actual game model

def convert_to_game_content(game: TicTacToe):
    game_content = dict()
    content_board = []
    for row in range(ROWS_N):
        for col in range(COLS_N):
            cell: Cell = game.board.get_cell(col, row)
            content_board.append({'col': col, 'row': row, 'color': cell.color, 'marked': 1 if cell.marked else 0})
    game_content['board'] = content_board
    game_content['state'] = game.state
    game_content['turn'] = game.turn
    return json.dumps(game_content)

def convert_to_game(game_content: dict):
    game = TicTacToe()
    content_board = game_content['board']
    cells = [list(Cell(CELL_EMPTY) for _ in range(COLS_N)) for _ in range(ROWS_N)]
    for content_cell in content_board:
        content_cell: dict
        col = content_cell['col']
        row = content_cell['row']
        color = content_cell['color']
        cell = Cell(color)
        cell.marked = content_cell['marked']
        cells[col][row] = cell
    board = Board()
    board.load_cells(cells)
    state = game_content['state']
    turn = game_content['turn']
    game.load_game(board, state, turn)
    return game
