import itertools
import pickle

import numpy
import pygame


# Main logic of tic tac toe game
class GameController:

    def __init__(self, players, shape, number_of_games):
        self.players = players
        self.shape = shape
        self.number_of_games = number_of_games
        self.running = True
        self.winner = ""
        self.episode = 0
        self.player_iterator = itertools.cycle(self.players)
        self.current_player = next(self.player_iterator)
        self.markers = {players[0].name: "X", players[1].name: "O"}
        self.grid = numpy.full((shape, shape), '-', dtype=str)
        self.stats = {player: {'win': 0, 'loss': 0, 'draw': 0} for player in players}

    # reset game properties
    def restart_game(self):
        self.grid = numpy.full((self.shape, self.shape), '-', dtype=str)
        self.running = True
        self.winner = ""

    # returns list of possible moves on the grid
    def possible_moves(self) -> list:
        row, col = numpy.where(self.grid == '-')

        return list(zip(row, col))

    # check if game is over, returns winner's name or "DRAW" in case of draw
    def check_grid(self) -> str:

        # diagonal and anti-diagonal check
        diagonal = self.grid[0][0] + self.grid[1][1] + self.grid[2][2]
        anti_diagonal = self.grid[2][0] + self.grid[1][1] + self.grid[0][2]

        if (diagonal == "XXX" or diagonal == "OOO") or (anti_diagonal == "XXX" or anti_diagonal == "OOO"):
            return self.current_player.name

        # x and y axis checking
        for row in range(0, 3):
            x_axis = ""
            y_axis = ""
            for col in range(0, 3):
                x_axis += self.grid[row][col]
                y_axis += self.grid[col][row]
            if (x_axis == "OOO" or x_axis == "XXX") or (y_axis == "OOO" or y_axis == "XXX"):
                return self.current_player.name

        if len(self.possible_moves()) == 0:
            return "DRAW"

        return ""

    # allows players to mark grid
    def make_move(self, move, update_grid=None):
        row, col = move

        self.grid[row][col] = self.markers[self.current_player.name]

        if update_grid is not None:
            update_grid(self.current_player, row, col)

    # simulate state after move, needed for exploitation
    def simulate_next_grid(self, move):
        row, col = move

        grid_copy = self.grid.copy()

        grid_copy[row][col] = self.markers[self.current_player.name]

        return grid_copy

    # generating string key from grid layout
    @staticmethod
    def generate_state_key(grid) -> str:

        return "".join(itertools.chain(*grid.tolist()))

    # distributes rewards between players
    def distribute_rewards(self) -> float:
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

    # main game loop
    def game_loop(self, update_grid=None, update_stats=None):

        while self.episode < self.number_of_games:
            self.restart_game()

            while self.running:
                state_to_estimate = self.generate_state_key(self.grid)

                self.make_move(self.current_player.mark_grid(self), update_grid)

                state_after_action = self.generate_state_key(self.grid)

                self.winner = self.check_grid()
                self.distribute_rewards()

                for player in self.players:
                    player.update_state_value(state_to_estimate, state_after_action)

                self.current_player = next(self.player_iterator)

                if self.winner != "":
                    self.running = False
                    self.episode += 1
                    self.count_stats()

                    if update_stats is not None:
                        update_stats()

                pygame.display.flip()

        # saving value function after each training sequence
        with open('../trained_bots/td-learning.pkl', 'wb') as file:
            pickle.dump(self.players[0], file)
