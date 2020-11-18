class GameState:

    def __init__(self, game):
        self.board = [row[:] for row in game.board]  # make a deep copy of the game board
        self.turn = 0
        self.ROWS = game.ROWS
        self.COLS = game.COLS
        self.PLAYERS = 2
        self.winner = None
        self.TO_WIN = game.TO_WIN

    # I changed this is_win function so that it didn't rely on a specific row/column
    def is_win(self, player):
        for col in range(self.COLS):
            c = 0
            for row in range(self.ROWS):
                if self.board[row][col] == player:
                    c += 1
                    if c == self.TO_WIN:
                        self.winner = player
                        return True
                else:
                    c = 0

        # horizontal
        for row in range(self.ROWS):
            c = 0
            for col in range(self.COLS):
                if self.board[row][col] == player:
                    c += 1
                    if c == self.TO_WIN:
                        self.winner = player
                        return True
                else:
                    c = 0

        # diagonal /
        for col in range(self.COLS - (self.TO_WIN - 1)):
            for row in range(self.ROWS - (self.TO_WIN - 1)):
                if self.board[row][col] == player and self.board[row + 1][col + 1] == player and self.board[row + 2][col + 2] == player and self.board[row + 3][col + 3] == player:
                    return True

        # diagonal \
        for col in range(self.COLS - (self.TO_WIN - 1)):
            for row in range(self.TO_WIN - 1, self.ROWS):
                if self.board[row][col] == player and self.board[row - 1][col + 1] == player and self.board[row - 2][col + 2] == player and self.board[row - 3][col + 3] == player:
                    return True
        return False

    def is_tie(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.board[i][j] is None:
                    return False
        return True

    def next_valid(self, col):
        if self.board[0][col] is None:
            for row in range(self.ROWS - 1, -1, -1):
                if self.board[row][col] is None:
                    return row
        return None

    def get_successors(self):
        successor_list = []  # list of coordinates
        for col in range(self.COLS):
            row = self.next_valid(col)
            if row is not None:
                successor_list.append((row, col))
        return successor_list

    def get_score(self):  # will write this
        # heuristic is based on the number of twos and threes in a row (for the computer)
        # could implement different heuristics as part of report
        return 1


def minimax(game):
    game_state = GameState(game)
    return max_value(game_state, 0, 5)


def max_value(game_state, num_moves, max_depth):
    if game_state.is_win(1):
        return [None, 100]  # computer wins
    elif game_state.is_win(0):
        return [None, -100]  # player wins
    elif game_state.is_tie():
        return [None, 0]  # not sure what score for tie should be
    elif num_moves > max_depth:
        return [None, game_state.get_score()]
    cur_max = -999999999
    move = None
    # print(game_state.board)
    # print(game_state.get_successors())
    for successor in game_state.get_successors():
        row = successor[0]
        col = successor[1]
        new_game_state = GameState(game_state)
        new_game_state.board[row][col] = 1  # computer move
        new_max = min_value(new_game_state, num_moves + 1, max_depth)[1]
        if new_max >= cur_max:
            cur_max = new_max
            move = successor
    return [move, cur_max]


def min_value(game_state, num_moves, max_depth):
    if game_state.is_win(1):
        return [None, 100]  # computer wins
    elif game_state.is_win(0):
        return [None, -100]  # player wins
    elif game_state.is_tie():
        return [None, 0]  # not sure what score for tie should be
    elif num_moves > max_depth:
        return [None, game_state.get_score()]
    cur_min = 999999999
    move = None
    for successor in game_state.get_successors():
        row = successor[0]
        col = successor[1]
        new_game_state = GameState(game_state)
        new_game_state.board[row][col] = 0  # player move
        new_min = max_value(new_game_state, num_moves + 1, max_depth)[1]
        if new_min <= cur_min:
            cur_min = new_min
            move = successor
    return [move, cur_min]


import game
testgame = game.ConnectFour()
gamestate = GameState(testgame)
print(minimax(gamestate))

