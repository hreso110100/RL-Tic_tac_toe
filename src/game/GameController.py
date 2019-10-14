import pickle
import time
from itertools import chain, cycle, islice

import matplotlib.pyplot as plt
import pygame
from numpy import where, full

from src.players.agents.NeuralNetworkBot import NeuralNetworkBot
from src.players.agents.TDBot import TDBot


# Main logic of tic tac toe game
class GameController:
    sum_reward = 0
    reward_list = []

    def __init__(self, players, shape, number_of_games):
        self.players = players
        self.shape = shape
        self.number_of_games = number_of_games
        self.running = True
        self.winner = ""
        self.episode = 0
        self.current_player = None
        self.player_switcher = None
        self.starting_player_index = 0
        self.markers = {players[0]: "X", players[1]: "O"}
        self.board = full((shape, shape), '-', dtype=str)
        self.stats = {player: {'win': 0, 'loss': 0, 'draw': 0} for player in players}

    # reset game properties
    def restart_game(self):
        self.board = full((self.shape, self.shape), '-', dtype=str)
        self.running = True
        self.player_switcher = islice(cycle(self.players), self.starting_player_index, None)
        self.starting_player_index = 1 - self.starting_player_index
        self.current_player = next(self.player_switcher)
        self.winner = ""

    # returns list of possible moves on the board
    def possible_moves(self) -> list:
        row, col = where(self.board == '-')

        return list(zip(row, col))

    # check if game is over, returns winner's name or "DRAW" in case of draw
    def check_board(self) -> str:
        diagonal = ""
        anti_diagonal = ""
        anti_diagonal_counter = self.shape - 1

        for i in range(0, self.shape):
            diagonal += self.board[i][i]
            anti_diagonal += self.board[i][anti_diagonal_counter]
            anti_diagonal_counter -= 1

        if (diagonal == (self.shape * "X") or diagonal == (self.shape * "O")) \
                or (anti_diagonal == (self.shape * "X") or anti_diagonal == (self.shape * "O")):
            return self.current_player.name

        # x and y axis checking
        for row in range(0, self.shape):
            x_axis = ""
            y_axis = ""
            for col in range(0, self.shape):
                x_axis += self.board[row][col]
                y_axis += self.board[col][row]

            if (x_axis == (self.shape * "O") or x_axis == (self.shape * "X")) \
                    or (y_axis == (self.shape * "O") or y_axis == (self.shape * "X")):
                return self.current_player.name

        if len(self.possible_moves()) == 0:
            return "DRAW"

        return ""

    # allows players to mark board
    def make_move(self, move, update_board=None):
        row, col = move

        self.board[row][col] = self.markers[self.current_player]

        if update_board is not None:
            update_board(self.current_player, row, col)

    # simulate state after move, needed for exploitation
    def simulate_next_board(self, move):
        row, col = move

        board_copy = self.board.copy()

        board_copy[row][col] = self.markers[self.current_player]

        return board_copy

    # generating string key from board and next state in case of Q-function
    @staticmethod
    def generate_board_key(board) -> str:

        return "".join(chain(*board.tolist()))

    # distributes rewards between players
    def distribute_rewards(self):
        if self.winner == "DRAW":
            for player in self.players:
                player.reward = 0.5

        elif self.winner == "":
            for player in self.players:
                player.reward = 0.0

        else:
            if self.winner == self.players[0].name:
                self.players[0].reward = 1.0
                self.players[1].reward = -1.0
            else:
                self.players[0].reward = -1.0
                self.players[1].reward = 1.0

    # counting stats about players
    def count_stats(self):
        if self.winner == "DRAW":
            self.stats[self.players[0]]['draw'] += 1
            self.stats[self.players[1]]['draw'] += 1
        elif self.winner == self.players[0].name:
            self.stats[self.players[0]]['win'] += 1
            self.stats[self.players[1]]['loss'] += 1
        else:
            self.stats[self.players[0]]['loss'] += 1
            self.stats[self.players[1]]['win'] += 1
        self.sum_reward += self.players[0].reward
        self.reward_list.append(self.sum_reward)

    # generating plots
    def generate_plot(self):
        fig, ax = plt.subplots()
        ax.plot(self.reward_list, 'r', label=f"{self.players[0].name}")
        ax.set(xlabel="epizóda", ylabel="celková odmena", title="Celková odmena počas epizódy")
        ax.grid()
        plt.legend(loc='upper left')
        plt.draw()
        fig.savefig(f'../graphs/{self.players[0].name}.png', dpi=1200)

    # update agent's estimates and counts stats
    def finalize(self, s, s_, update_stats):
        if type(self.players[0]) is NeuralNetworkBot:
            self.players[0].store_experience(
                [s, self.players[0].action, s_, self.players[0].reward, self.winner])

            if len(self.players[0].memory) >= self.players[0].min_batch_size:
                self.players[0].update(self)
                self.players[0].update_epsilon()
        else:
            self.players[0].update(s, s_, self)
        self.running = False
        self.episode += 1
        self.count_stats()
        if update_stats is not None:
            update_stats()

    # game loop for td(0)
    def td_game_loop(self, update_board, update_stats):
        to_estimate = self.generate_board_key(self.board)
        self.make_move(self.current_player.mark(self), update_board)
        after_action = self.generate_board_key(self.board)

        self.winner = self.check_board()
        self.distribute_rewards()

        for player in self.players:
            player.update(to_estimate, after_action, self)

        self.current_player = next(self.player_switcher)

        if self.winner != "":
            self.running = False
            self.episode += 1
            self.count_stats()

            if update_stats is not None:
                update_stats()
        pygame.display.flip()

    # main game loop
    def game_loop(self, update_board=None, update_stats=None):
        start_time = time.time()

        # just in case learner is TD(0)
        if type(self.players[0]) is TDBot:
            while self.episode < self.number_of_games:
                self.restart_game()

                while self.running:
                    self.td_game_loop(update_board, update_stats)

        # others game loop
        else:
            while self.episode < self.number_of_games:
                print(f"Episode: {self.episode}")
                self.restart_game()

                if self.players[1].name == self.current_player.name:
                    self.make_move(self.current_player.mark(self), update_board)
                    self.current_player = next(self.player_switcher)
                    pygame.display.flip()

                while self.running:
                    s = self.generate_board_key(self.board)
                    self.make_move(self.current_player.mark(self), update_board)
                    s_ = self.generate_board_key(self.board)
                    self.winner = self.check_board()
                    self.distribute_rewards()

                    if self.winner == "":
                        self.current_player = next(self.player_switcher)
                        pygame.display.flip()
                        self.make_move(self.current_player.mark(self), update_board)
                        s_ = self.generate_board_key(self.board)
                        self.winner = self.check_board()
                        self.distribute_rewards()

                        if self.winner == "":
                            if type(self.players[0]) is NeuralNetworkBot:
                                self.players[0].store_experience(
                                    [s, self.players[0].action, s_, self.players[0].reward, self.winner])
                            else:
                                self.players[0].update(s, s_, self)
                            self.current_player = next(self.player_switcher)
                            pygame.display.flip()
                        else:
                            self.finalize(s, s_, update_stats)
                    else:
                        self.finalize(s, s_, update_stats)

                pygame.display.flip()

        print("###############\n" + "Training duration: " + str(
            round(time.time() - start_time, 2)) + " seconds. \n###############")

        # saving objects after each training sequence
        with open(f'../trained_bots/{self.players[0].name}.pkl', 'wb') as file:
            pickle.dump(self.players[0], file)
