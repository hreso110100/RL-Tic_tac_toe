import random

from src.players.CommonPlayer import CommonPlayer


class ApproximateQBot(CommonPlayer):

    def __init__(self, name):
        super().__init__(name)
        self.initial_values = 0
        self.features_weights = {
            self.bias: self.initial_values,
            self.feature_1: self.initial_values,
            self.feature_2: self.initial_values,
            self.feature_3: self.initial_values,
            self.feature_4: self.initial_values
        }

    # simulate state after taking action
    def simulate(self, state, action, marker):
        listed = list(state)
        listed[action[0] * 4 + action[1]] = marker
        return "".join(listed)

    # bias
    def bias(self, state, action, game) -> float:
        return 1.0

    # agent action to win
    def feature_1(self, state, action, game) -> float:
        bot_marker = game.markers[game.players[0].name]
        opponent_marker = game.markers[game.players[1].name]
        sim_state = self.simulate(state, action, bot_marker)

        if game.players[1].action is not None:
            sim_state = self.simulate(sim_state, action, opponent_marker)

        # checking marked row
        row = sim_state[4 * action[0]: 4 * action[1] + 4]

        if opponent_marker not in row and 4 * bot_marker in row:
            return 1

        # checking marked col
        col = ""

        for j in range(action[1], 16, 4):
            col += sim_state[j]

        if opponent_marker not in col and 4 * bot_marker in col:
            return 1

        # checking marked diagonal
        diagonal_action = [(0, 0), (1, 1), (2, 2), (3, 3)]

        if action in diagonal_action:
            diagonal = sim_state[0] + sim_state[5] + sim_state[10] + sim_state[15]

            if opponent_marker not in diagonal and 4 * bot_marker in diagonal:
                return 1

        # checking marked anti-diagonal

        anti_diagonal_action = [(0, 3), (1, 2), (2, 1), (3, 0)]

        if action in anti_diagonal_action:
            anti_diagonal = sim_state[3] + sim_state[6] + sim_state[9] + sim_state[12]

            if opponent_marker not in anti_diagonal and 4 * bot_marker in anti_diagonal:
                return 1

        return 0

    # checking if action blocks opponent move
    def feature_2(self, state, action, game):
        bot_marker = game.markers[game.players[0].name]
        opponent_marker = game.markers[game.players[1].name]
        sim_state = self.simulate(state, action, bot_marker)

        if game.players[1].action is not None:
            sim_state = self.simulate(sim_state, action, opponent_marker)

        # checking marked row
        row = sim_state[4 * action[0]: 4 * action[1] + 4]

        if row.count(opponent_marker) == 3 and bot_marker in row:
            return 1

        # checking marked col
        col = ""

        for j in range(action[1], 16, 4):
            col += sim_state[j]

        if col.count(opponent_marker) == 3 and bot_marker in col:
            return 1

        # checking marked diagonal
        diagonal_action = [(0, 0), (1, 1), (2, 2), (3, 3)]

        if action in diagonal_action:
            diagonal = sim_state[0] + sim_state[5] + sim_state[10] + sim_state[15]

            if diagonal.count(opponent_marker) == 3 and bot_marker in diagonal:
                return 1

        # checking marked anti-diagonal

        anti_diagonal_action = [(0, 3), (1, 2), (2, 1), (3, 0)]

        if action in anti_diagonal_action:
            anti_diagonal = sim_state[3] + sim_state[6] + sim_state[9] + sim_state[12]

            if anti_diagonal.count(opponent_marker) == 3 and bot_marker in anti_diagonal:
                return 1

        return 0

    # agent percentage to win
    def feature_3(self, state, action, game) -> float:
        percentage = [0]
        bot_marker = game.markers[game.players[0].name]
        opponent_marker = game.markers[game.players[1].name]
        sim_state = self.simulate(state, action, bot_marker)

        # row check
        start_index = 0

        for last_index in range(4, 20, 4):
            if opponent_marker not in sim_state[start_index:last_index] \
                    and bot_marker in sim_state[start_index:last_index]:
                percentage.append(sim_state[start_index:last_index].count(bot_marker) * 0.25)

            start_index = last_index

        # col check

        for i in range(0, 4):
            col_state = ""
            for j in range(i, 16, 4):
                col_state += sim_state[j]
            if opponent_marker not in col_state and bot_marker in col_state:
                percentage.append(col_state.count(bot_marker) * 0.25)

            # diagonal check

        diagonal_state = sim_state[0] + sim_state[5] + sim_state[10] + sim_state[15]

        if opponent_marker not in diagonal_state and bot_marker in diagonal_state:
            percentage.append(diagonal_state.count(bot_marker) * 0.25)

        # anti-diagonal check

        anti_diagonal_state = sim_state[3] + sim_state[6] + sim_state[9] + sim_state[12]

        if opponent_marker not in anti_diagonal_state and bot_marker in anti_diagonal_state:
            percentage.append(anti_diagonal_state.count(bot_marker) * 0.25)

        return max(percentage)

    # opponent percentage to win
    def feature_4(self, state, action, game) -> float:
        percentage = [0]
        bot_marker = game.markers[game.players[0].name]
        opponent_marker = game.markers[game.players[1].name]
        sim_state = self.simulate(state, action, bot_marker)

        # row check
        start_index = 0

        for last_index in range(4, 20, 4):
            if opponent_marker in sim_state[start_index:last_index] and bot_marker not in sim_state[
                                                                                          start_index:last_index]:
                percentage.append(sim_state[start_index:last_index].count(opponent_marker) * 0.25)

            start_index = last_index

        # col check

        for i in range(0, 4):
            col_state = ""
            for j in range(i, 16, 4):
                col_state += sim_state[j]
            if opponent_marker in col_state and bot_marker not in col_state:
                percentage.append(col_state.count(opponent_marker) * 0.25)

            # diagonal check

        diagonal_state = sim_state[0] + sim_state[5] + sim_state[10] + sim_state[15]

        if opponent_marker in diagonal_state and bot_marker not in diagonal_state:
            percentage.append(diagonal_state.count(opponent_marker) * 0.25)

        # anti-diagonal check

        anti_diagonal_state = sim_state[3] + sim_state[6] + sim_state[9] + sim_state[12]

        if opponent_marker in anti_diagonal_state and bot_marker not in anti_diagonal_state:
            percentage.append(anti_diagonal_state.count(opponent_marker) * 0.25)

        return max(percentage)

    # making move
    def mark(self, game) -> tuple:
        self.print_estimates(game)

        if random.random() < self.epsilon:
            # Exploration
            self.epsilon -= (self.epsilon / 1_000)
            self.action = random.choice(game.possible_moves())

            return self.action

        else:
            # Exploitation
            options = []
            s = game.generate_board_key(game.board)

            for position in game.possible_moves():
                value = self.get_estimates(s, position, game)
                options.append((value, position))

            max_value = max(options)[0]
            best_options = [option for option in options if option[0] == max_value]
            self.action = random.choice(best_options)[1]

            return self.action

    # printing values of free cells
    def print_estimates(self, game):

        for move in game.possible_moves():
            print(move, self.get_estimates(game.generate_board_key(game.board), move, game))

    # selecting max action from s(t+1)
    def select_max_action(self, s_, game) -> float:
        options = []

        for action in game.possible_moves():
            options.append(self.get_estimates(s_, action, game))

        if len(options) > 0:
            return max(options)
        else:
            return 0.0

    # calculating Q values
    def get_estimates(self, state, action, game) -> float:
        results = 0

        for feature, weight in self.features_weights.items():
            results += (feature(state, action, game) * weight)

        return results

    # updating weights
    def update(self, s, s_, game):
        max_action = self.select_max_action(s_, game)

        for feature, weight in self.features_weights.items():
            self.features_weights[feature] = weight + self.alpha * \
                                             (self.reward + (self.gamma * max_action) - self.get_estimates(
                                                 s, self.action, game)) * feature(s, self.action, game)
