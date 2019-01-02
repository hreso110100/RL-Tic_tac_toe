import pygame

from src.players.CommonPlayer import CommonPlayer


class Human(CommonPlayer):

    def mark_grid(self, game_controller) -> tuple:

        row = col = None
        not_valid_move = True

        while not_valid_move:
            mouse_position = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # row = 0, col = 0
                    if 130 > mouse_position[0] > 10 and 130 > mouse_position[1] > 10:
                        row = col = 0

                    # row = 0, col = 1
                    elif 250 > mouse_position[0] > 130 and 130 > mouse_position[1] > 10:
                        row = 0
                        col = 1
                    # row = 0, col = 2
                    elif 370 > mouse_position[0] > 250 and 130 > mouse_position[1] > 10:
                        row = 0
                        col = 2

                    # row = 1, col = 0
                    elif 130 > mouse_position[0] > 10 and 250 > mouse_position[1] > 130:
                        row = 1
                        col = 0

                    # row = 1, col = 1
                    elif 250 > mouse_position[0] > 130 and 250 > mouse_position[1] > 130:
                        row = 1
                        col = 1

                    # row = 1, col = 2
                    elif 370 > mouse_position[0] > 250 and 250 > mouse_position[1] > 130:
                        row = 1
                        col = 2

                    # row = 2, col = 0
                    elif 130 > mouse_position[0] > 10 and 370 > mouse_position[1] > 250:
                        row = 2
                        col = 0

                    # row = 2, col = 1
                    elif 250 > mouse_position[0] > 130 and 370 > mouse_position[1] > 250:
                        row = 2
                        col = 1

                    # row = 2, col = 2
                    elif 370 > mouse_position[0] > 250 and 370 > mouse_position[1] > 250:
                        row = 2
                        col = 2

                    if (row, col) in game_controller.possible_moves():
                        not_valid_move = False
                        break

        return row, col
