import random

from src.players.CommonPlayer import CommonPlayer


class QBot(CommonPlayer):

    def __init__(self, name, q_function=None):
        super().__init__(name)
        self.initial_values = 0.5
        if q_function is None:
            q_function = {}
        self.q_function = q_function

    def mark(self, game) -> tuple:
        self.print_estimates(game)

        if random.random() < self.epsilon:
            # Exploration
            self.epsilon -= (self.epsilon / 10_000)
            self.action = random.choice(game.possible_moves())

            return self.action

        else:
            # Exploitation
            options = []
            for position in game.possible_moves():
                current_state_key = game.generate_board_key(game.board)
                action_state_value = self.get_estimates((current_state_key, position))
                options.append((action_state_value, position))

            max_value = max(options)[0]
            best_options = [option for option in options if option[0] == max_value]
            self.action = random.choice(best_options)[1]

            return self.action

    def select_max_action(self, state, game):
        options = []

        for action in game.possible_moves():
            options.append(self.get_estimates((state, action)))

        if len(options) > 0:
            return max(options)
        else:
            return 0.0

    def print_estimates(self, game):
        for move in game.possible_moves():
            print(move, self.get_estimates((game.generate_board_key(game.board), move)))

    def update(self, s, s_, game):
        max_action = self.select_max_action(s_, game)
        q_s = self.get_estimates((s, self.action))

        self.q_function[(s, self.action)] = q_s + self.alpha * (
                self.reward + (self.gamma * max_action) - q_s)

    def get_estimates(self, board_action) -> float:
        return self.q_function.get(board_action, self.initial_values)
