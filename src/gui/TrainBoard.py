import pygame

from src.game.GameController import GameController
from src.gui.CommonSurface import CommonSurface
from src.players.opponents.Human import Human


class TrainBoard(CommonSurface):

    def __init__(self, main_surface, board_shape):
        super().__init__(main_surface)
        self.board_shape = board_shape
        self.game_controller = None

    def generate_surface(self, game_controller=None) -> str:
        self.clear_surface()

        self.current_screen = "TRAIN_BOARD"
        self.game_controller = game_controller

        current_episode_text = self.font_big.render("EPISODE : ", False, CommonSurface.BLUE)
        self.main_surface.blit(current_episode_text, (10, 10))
        current_episode_value = self.font_big.render(f"{self.game_controller.episode}", False, CommonSurface.WHITE)
        self.main_surface.blit(current_episode_value, (240, 10))

        stats_text = self.font_big.render("STATS", False, CommonSurface.BLUE)
        self.main_surface.blit(stats_text, (10, 120))

        win_text = self.font_big.render("WIN", False, CommonSurface.WHITE)
        self.main_surface.blit(win_text, (190, 120))

        win_learner_value = self.font_medium.render(
            f"{self.game_controller.stats[self.game_controller.players[0]]['win']}",
            False, CommonSurface.BLUE)
        self.main_surface.blit(win_learner_value, (190, 200))

        win_trainer_value = self.font_medium.render(
            f"{self.game_controller.stats[self.game_controller.players[1]]['win']}", False, CommonSurface.WHITE)
        self.main_surface.blit(win_trainer_value, (190, 260))

        draw_text = self.font_big.render("DRAW", False, CommonSurface.WHITE)
        self.main_surface.blit(draw_text, (310, 120))

        draw_learner_value = self.font_medium.render(
            f"{self.game_controller.stats[self.game_controller.players[0]]['draw']}",
            False, CommonSurface.BLUE)
        self.main_surface.blit(draw_learner_value, (310, 200))

        draw_trainer_value = self.font_medium.render(
            f"{self.game_controller.stats[self.game_controller.players[1]]['draw']}",
            False, CommonSurface.WHITE)
        self.main_surface.blit(draw_trainer_value, (310, 260))

        loss_text = self.font_big.render("LOSS", False, CommonSurface.WHITE)
        self.main_surface.blit(loss_text, (460, 120))

        loss_learner_value = self.font_medium.render(
            f"{self.game_controller.stats[self.game_controller.players[0]]['loss']}", False, CommonSurface.BLUE)
        self.main_surface.blit(loss_learner_value, (460, 200))

        loss_trainer_value = self.font_medium.render(
            f"{self.game_controller.stats[self.game_controller.players[1]]['loss']}", False, CommonSurface.WHITE)
        self.main_surface.blit(loss_trainer_value, (460, 260))

        algorithm_value = self.font_medium.render(f"{self.game_controller.players[0].name}", False,
                                                  CommonSurface.WHITE)
        self.main_surface.blit(algorithm_value, (10, 200))

        algorithm_value = self.font_medium.render(f"{self.game_controller.players[1].name}", False,
                                                  CommonSurface.WHITE)
        self.main_surface.blit(algorithm_value, (10, 260))

        pygame.display.flip()

        # running a training
        self.game_controller.game_loop(update_stats=self.update_stats)

        # generating plots
        game_controller.generate_plot()

        # displaying buttons after training was completed

        test_button_text = self.font_small.render("Test performance", False, CommonSurface.WHITE)
        pygame.draw.rect(self.main_surface, CommonSurface.BLUE, (440, 350, 150, 40))
        self.main_surface.blit(test_button_text, (450, 360))

        menu_button_text = self.font_small.render("Main Menu", False, CommonSurface.BLUE)
        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, (10, 350, 150, 40))
        self.main_surface.blit(menu_button_text, (45, 360))

        return self.current_screen

    def handle_clicks(self, mouse_position, class_to_switch) -> str:

        # test performance button
        if 590 > mouse_position[0] > 440 and 390 > mouse_position[1] > 350:

            learner = self.game_controller.players[0]
            learner.epsilon = 0

            self.game_controller = GameController(players=[learner, Human("Human")], shape=self.game_controller.shape,
                                                  number_of_games=1)
            self.current_screen = class_to_switch[1].generate_surface(self.game_controller)

        # main menu button
        elif 160 > mouse_position[0] > 10 and 390 > mouse_position[1] > 40:
            self.current_screen = class_to_switch[0].generate_surface()

        return self.current_screen

    def update_stats(self):
        self.main_surface.fill(CommonSurface.GREY, (240, 10, 300, 50))
        current_episode_value = self.font_big.render(f"{self.game_controller.episode}", False, CommonSurface.WHITE)
        self.main_surface.blit(current_episode_value, (240, 10))

        self.main_surface.fill(CommonSurface.GREY, (310, 200, 100, 50))
        draw_learner_value = self.font_medium.render(
            f"{self.game_controller.stats[self.game_controller.players[0]]['draw']}",
            False, CommonSurface.BLUE)
        self.main_surface.blit(draw_learner_value, (310, 200))

        self.main_surface.fill(CommonSurface.GREY, (310, 260, 100, 50))
        draw_trainer_value = self.font_medium.render(
            f"{self.game_controller.stats[self.game_controller.players[1]]['draw']}",
            False, CommonSurface.WHITE)
        self.main_surface.blit(draw_trainer_value, (310, 260))

        self.main_surface.fill(CommonSurface.GREY, (190, 200, 100, 50))
        win_learner_value = self.font_medium.render(
            f"{self.game_controller.stats[self.game_controller.players[0]]['win']}",
            False, CommonSurface.BLUE)
        self.main_surface.blit(win_learner_value, (190, 200))

        self.main_surface.fill(CommonSurface.GREY, (190, 260, 100, 50))
        win_trainer_value = self.font_medium.render(
            f"{self.game_controller.stats[self.game_controller.players[1]]['win']}", False, CommonSurface.WHITE)
        self.main_surface.blit(win_trainer_value, (190, 260))

        self.main_surface.fill(CommonSurface.GREY, (460, 200, 100, 50))
        loss_learner_value = self.font_medium.render(
            f"{self.game_controller.stats[self.game_controller.players[0]]['loss']}", False, CommonSurface.BLUE)
        self.main_surface.blit(loss_learner_value, (460, 200))

        self.main_surface.fill(CommonSurface.GREY, (460, 260, 100, 50))
        loss_trainer_value = self.font_medium.render(
            f"{self.game_controller.stats[self.game_controller.players[1]]['loss']}", False, CommonSurface.WHITE)
        self.main_surface.blit(loss_trainer_value, (460, 260))

