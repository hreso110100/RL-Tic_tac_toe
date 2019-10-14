import random

from src.game.GameController import GameController
from src.players.CommonPlayer import CommonPlayer


class RandomBot(CommonPlayer):

    def __init__(self, name):
        super().__init__(name)

    def mark(self, game: GameController) -> tuple:
        marker = game.markers[self]

        for move in game.possible_moves():
            sim_board = game.simulate_next_board(move)

            diagonal = ""
            anti_diagonal = ""
            anti_diagonal_counter = game.shape - 1

            for i in range(0, game.shape):
                diagonal += sim_board[i][i]
                anti_diagonal += sim_board[i][anti_diagonal_counter]
                anti_diagonal_counter += -1

            if (diagonal == (game.shape * marker)) or (anti_diagonal == (game.shape * marker)):
                self.action = move
                return self.action

            # x and y axis checking
            for row in range(0, game.shape):
                x_axis = ""
                y_axis = ""
                for col in range(0, game.shape):
                    x_axis += sim_board[row][col]
                    y_axis += sim_board[col][row]

                if (x_axis == (game.shape * marker)) or (y_axis == (game.shape * marker)):
                    self.action = move
                    return self.action

        self.action = random.choice(game.possible_moves())
        return self.action

    def update(self, s, s_, game):
        pass

    def get_estimates(self, board) -> float:
        pass

    def print_estimates(self, game):
        pass
