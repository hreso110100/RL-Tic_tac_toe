import pygame

from src.gui.CommonSurface import CommonSurface


class Board(CommonSurface):
    current_turn_value = ""

    def __init__(self, main_surface):
        super().__init__(main_surface)
        self.grid_surface = pygame.Surface((360, 360))
        self.game_controller = None

    def generate_surface(self, game_controller=None) -> str:
        self.clear_surface()
        self.grid_surface.fill(CommonSurface.GREY)

        self.current_screen = "BOARD"
        self.game_controller = game_controller

        algorithm_text = self.font_medium.render("Opponent:", False, CommonSurface.BLUE)
        self.main_surface.blit(algorithm_text, (410, 30))
        algorithm_value = self.font_medium.render(f"{self.game_controller.players[0].name}", False,
                                                  CommonSurface.WHITE)
        self.main_surface.blit(algorithm_value, (410, 70))

        for x in range(0, 3):
            for y in range(0, 3):
                pygame.draw.rect(self.grid_surface, CommonSurface.WHITE, [120 * y, 120 * x, 120, 120], 1)

        self.main_surface.blit(self.grid_surface, (10, 10))

        pygame.display.flip()

        self.game_controller.game_loop(self.draw_marker)

        self.after_game()

        return self.current_screen

    # draws GUI content after game
    def after_game(self):
        restart_button_text = self.font_small.render("New Game", False, CommonSurface.WHITE)
        pygame.draw.rect(self.main_surface, CommonSurface.BLUE, (410, 290, 150, 30))
        self.main_surface.blit(restart_button_text, (445, 295))

        menu_button_text = self.font_small.render("Main Menu", False, CommonSurface.BLUE)
        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, (410, 340, 150, 30))
        self.main_surface.blit(menu_button_text, (445, 345))

        if self.game_controller.winner == "DRAW":
            winner_text = self.font_medium.render("It is draw !", False, CommonSurface.BLUE)
        else:
            winner_text = self.font_medium.render("Winner is :", False, CommonSurface.BLUE)
            winner_value = self.font_medium.render(f"{self.game_controller.winner}", False,
                                                   CommonSurface.WHITE)
            self.main_surface.blit(winner_value, (410, 190))

        self.main_surface.blit(winner_text, (410, 150))

    def handle_clicks(self, mouse_position, class_to_switch=None) -> str:

        # new game button
        if 560 > mouse_position[0] > 410 and 320 > mouse_position[1] > 290:
            self.game_controller.episode = 0
            self.current_screen = self.generate_surface(self.game_controller)

        # main menu button
        elif 560 > mouse_position[0] > 410 and 370 > mouse_position[1] > 340:
            self.current_screen = class_to_switch.generate_surface()

        return self.current_screen

    # draw x or o to the given coordinates
    def draw_marker(self, player, row, col):
        marker = self.game_controller.markers[player.name]

        if marker == "X":
            marker = self.cross
        else:
            marker = self.circle

        self.grid_surface.blit(marker, (col * 120, row * 120))
        self.main_surface.blit(self.grid_surface, (10, 10))
