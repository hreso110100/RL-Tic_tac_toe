import random

from src.players.CommonPlayer import CommonPlayer


class TDBot(CommonPlayer):

    def __init__(self, name, learning_rate=0.1, gamma=0.8, epsilon=0.9, initial_state_value=0.5, value_function=None):
        super().__init__(name)
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.initial_state_value = initial_state_value
        if value_function is None:
            value_function = {}
        self.value_function = value_function

    def mark_grid(self, game_controller) -> tuple:

        self.print_values(game_controller)

        if random.random() < self.epsilon:
            # Exploration
            self.epsilon *= 0.9

            return random.choice(game_controller.possible_moves())

        else:
            # Exploitation
            options = []
            for position in game_controller.possible_moves():
                next_state = game_controller.simulate_next_grid(position)
                next_state_key = game_controller.generate_state_key(next_state)
                state_value = self.get_state_value(next_state_key)
                options.append((state_value, position))

            max_value = max(options)[0]
            best_options = [option for option in options if option[0] == max_value]
            best_option = random.choice(best_options)[1]

            return best_option

    def print_values(self, game):
        for move in game.possible_moves():
            key = game.simulate_next_grid(move)

            print(move, self.get_state_value(game.generate_state_key(key)))

    def update_state_value(self, state_to_estimate, state_after_action):

        self.value_function[state_to_estimate] = self.get_state_value(state_to_estimate) + self.learning_rate * (
                self.reward + self.gamma * self.get_state_value(state_after_action)
                - self.get_state_value(state_to_estimate))

        # if there is no other possible state
        if self.reward == 1 or self.reward == -1 or self.reward == 0.5:
            self.value_function[state_after_action] = self.get_state_value(state_after_action) + self.learning_rate * (
                    self.reward - self.get_state_value(state_after_action))

    def get_state_value(self, state_key) -> float:
        return self.value_function.get(state_key, self.initial_state_value)
