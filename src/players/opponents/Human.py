import pygame

from src.players.CommonPlayer import CommonPlayer


class Human(CommonPlayer):

    def __init__(self, name):
        super().__init__(name)

    def mark(self, game) -> tuple:
        not_valid_move = True

        while not_valid_move:
            mouse_position = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    col, row = self.click(mouse_position, game)

                    if (row, col) in game.possible_moves():
                        self.action = row, col
                        not_valid_move = False
                        break

        return self.action

    def click(self, mouse_position, game):
        j = i = 0
        rect_size = 360 / game.shape

        for i in range(0, game.shape):
            for j in range(0, game.shape):
                if ((j + 1) * rect_size + 10) > mouse_position[0] > (j * rect_size + 10) and \
                        ((i + 1) * rect_size + 10) > mouse_position[1] > (i * rect_size + 10):
                    return j, i

        return j, i

    def update(self, s, s_, game):
        pass

    def get_estimates(self, board) -> float:
        pass

    def print_estimates(self, game):
        pass
