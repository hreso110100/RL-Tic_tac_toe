import random

from src.players.CommonPlayer import CommonPlayer


class RandomBot(CommonPlayer):

    def mark_grid(self, game_controller) -> tuple:
        return random.choice(game_controller.possible_moves())
