import copy
import random
from itertools import chain

import numpy as np
from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

from src.game import GameController


class NeuralNetworkBot:

    def __init__(self, name: str):
        self.name = name
        self.memory = list()
        self.buffer_size = 10000
        self.batch_size = 64
        self.min_batch_size = 1000
        self.alpha = 0.0001
        self.gamma = 0.7
        self.tau = 0.1
        self.epsilon = 0.9
        self.epsilon_decay = 0.95
        self.epsilon_min = 0.1
        self.action = None
        self.reward = None
        self.model = None
        self.target_model = None

    # create DQN model
    def create_model(self, game: GameController) -> Sequential:
        input_size = (game.shape ** 2) * 3

        model = Sequential()
        model.add(Dense(64, input_dim=input_size, activation='relu', kernel_initializer="random_uniform"))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense((game.shape ** 2), activation='linear'))
        model.compile(loss="mse", optimizer=Adam(self.alpha))

        return model

    # creating one-hot-encoded array
    # TODO drop dummy variable
    def preprocess_input(self, board) -> list:
        encoded_x = copy.deepcopy(board).replace('X', '1').replace('O', '0').replace('-', '0')
        encoded_o = copy.deepcopy(board).replace('X', '0').replace('O', '1').replace('-', '0')
        encoded_blank = copy.deepcopy(board).replace('X', '0').replace('O', '0').replace('-', '1')

        chained_x = list(chain.from_iterable(encoded_x))
        chained_o = list(chain.from_iterable(encoded_o))
        chained_blank = list(chain.from_iterable(encoded_blank))

        string_board = list(chain(chained_x, chained_o, chained_blank))
        board_to_int = [int(element) for element in string_board]

        return np.reshape(board_to_int, (1, len(board_to_int)))

    # storing agent experience in FIFO replay memory
    def store_experience(self, experience: list):
        if len(self.memory) < self.buffer_size:
            self.memory.append(experience)
        else:
            self.memory.pop(0)
            self.store_experience(experience)

    # get one batch of given size
    def get_batch(self) -> list:
        return random.sample(self.memory, self.batch_size)

    # update epsilon
    def update_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

    def mark(self, game: GameController) -> tuple:

        if random.random() < self.epsilon:
            # Exploration
            self.action = random.choice(game.possible_moves())

            return self.action

        else:
            # Exploitation
            options = []
            processed_input = self.preprocess_input(game.generate_board_key(game.board))
            q_values = self.model.predict(processed_input)

            for position in game.possible_moves():
                value = self.get_estimates(game, position, q_values)
                options.append((value, position))

            max_value = max(options)[0]
            best_options = [option for option in options if option[0] == max_value]
            self.action = random.choice(best_options)[1]

            return self.action

    # update Q-values from batch
    def update(self, game: GameController):
        mini_batch = self.get_batch()
        new_q_values = []

        for state, action, next_state, reward, winner in mini_batch:
            q_values_state = self.model.predict(self.preprocess_input(state))[0]

            if winner != "":
                target = reward
            else:
                # choosing max action from state_
                max_action = np.argmax(self.model.predict(self.preprocess_input(next_state)))
                # calculating target and Q(s_,a)
                target = reward + self.gamma * self.target_model.predict(self.preprocess_input(next_state))[0][
                    max_action]

            # updated Q values for specific action
            converted_action = (action[0] * game.shape) + action[1]
            q_values_state[converted_action] = target
            new_q_values.append(q_values_state)

        input_states = np.array([self.preprocess_input(sample[0])[0] for sample in mini_batch])
        self.model.fit(input_states, np.array(new_q_values), verbose=1, epochs=1, batch_size=self.batch_size)
        self.update_target_weights()

    # copy weights from model to target
    def update_target_weights(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()

        for index, (weight, target_weight) in enumerate(zip(weights, target_weights)):
            target_weight = weight * self.tau + target_weight * (1 - self.tau)
            target_weights[index] = target_weight

        self.target_model.set_weights(target_weights)

    # using DQN to retrieve Q values for each action in given state
    def get_estimates(self, game: GameController, action, q_values) -> float:
        converted_action = (action[0] * game.shape) + action[1]

        return q_values[0][converted_action]
