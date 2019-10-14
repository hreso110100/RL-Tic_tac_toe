import random

from src.players.CommonPlayer import CommonPlayer


class TDBot(CommonPlayer):

    def __init__(self, name, value_function=None):
        super().__init__(name)
        self.initial_values = 0.5

        if value_function is None:
            value_function = {}
        self.value_function = value_function

    def mark(self, game) -> tuple:
        self.print_estimates(game)

        if random.random() < self.epsilon:
            # Exploration
            self.epsilon *= 0.9

            return random.choice(game.possible_moves())

        else:
            # Exploitation
            options = []
            for position in game.possible_moves():
                next_state = game.simulate_next_board(position)
                next_state_key = game.generate_board_key(next_state)
                state_value = self.get_estimates(next_state_key)
                options.append((state_value, position))

            max_value = max(options)[0]
            best_options = [option for option in options if option[0] == max_value]
            best_option = random.choice(best_options)[1]

            return best_option

    def print_estimates(self, game):
        for move in game.possible_moves():
            key = game.simulate_next_board(move)

            print(move, self.get_estimates(game.generate_board_key(key)))

    def update(self, s, s_, game):

        self.value_function[s] = self.get_estimates(s) + self.alpha * (
                self.reward + self.gamma * self.get_estimates(s_)
                - self.get_estimates(s))

        # if there is no other possible state
        if self.reward == 1 or self.reward == -1 or self.reward == 0.5:
            self.value_function[s_] = self.get_estimates(s_) + self.alpha * (
                    self.reward - self.get_estimates(s_))

    def get_estimates(self, board) -> float:
        return self.value_function.get(board, self.initial_values)
