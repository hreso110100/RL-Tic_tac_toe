import pickle

import pygame

from src.game.GameController import GameController
from src.gui.CommonSurface import CommonSurface
from src.players.Human import Human
from src.players.QBot import QBot
from src.players.RandomBot import RandomBot
from src.players.TDBot import TDBot


class Settings(CommonSurface):
    learner = None
    trainer = None
    game_controller = None

    def __init__(self, main_surface):
        super().__init__(main_surface)

    def generate_surface(self, game_controller=None) -> str:
        self.clear_surface()
        self.current_screen = "SETTINGS"

        game_title_text = self.font_big.render("TIC TAC TOE", False, CommonSurface.WHITE)
        self.main_surface.blit(game_title_text, (170, 0))

        select_algorithm_text = self.font_medium.render("Select AI algorithm", False, CommonSurface.BLUE)
        self.main_surface.blit(select_algorithm_text, (10, 80))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [10, 130, 25, 25], 1)
        q_learning_text = self.font_medium.render("Q-learning", False, CommonSurface.WHITE)
        self.main_surface.blit(q_learning_text, (50, 125))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [210, 130, 25, 25], 1)
        td_learning_text = self.font_medium.render("TD learning", False, CommonSurface.WHITE)
        self.main_surface.blit(td_learning_text, (250, 125))

        choose_train_method_text = self.font_medium.render("Choose how to train ", False, CommonSurface.BLUE)
        self.main_surface.blit(choose_train_method_text, (10, 200))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [10, 250, 25, 25], 1)
        random_training_text = self.font_medium.render("Random", False, CommonSurface.WHITE)
        self.main_surface.blit(random_training_text, (50, 245))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [210, 250, 25, 25], 1)
        clone_training_text = self.font_medium.render("Clone", False, CommonSurface.WHITE)
        self.main_surface.blit(clone_training_text, (250, 245))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, (440, 300, 150, 40))
        load_td_bot_button = self.font_small.render("Load TDBot", False, CommonSurface.BLUE)
        self.main_surface.blit(load_td_bot_button, (470, 310))

        pygame.draw.rect(self.main_surface, CommonSurface.BLUE, (440, 350, 150, 40))
        train_button = self.font_small.render("Train AI", False, CommonSurface.WHITE)
        self.main_surface.blit(train_button, (480, 360))

        return self.current_screen

    def handle_clicks(self, mouse_position, class_to_switch=None) -> str:
        check_mark = pygame.image.load('../assets/check_mark.png')
        check_mark = pygame.transform.scale(check_mark, (25, 25))

        # Q-learning checkbox
        if 35 > mouse_position[0] > 10 and 155 > mouse_position[1] > 130:
            self.main_surface.blit(check_mark, (10, 130))
            self.main_surface.fill(CommonSurface.GREY, (211, 131, 23, 23))
            self.learner = QBot("Q-learning")

        # TD learning checkbox
        elif 235 > mouse_position[0] > 210 and 155 > mouse_position[1] > 130:
            self.main_surface.blit(check_mark, (210, 130))
            self.main_surface.fill(CommonSurface.GREY, (11, 131, 23, 23))
            self.learner = TDBot("TD-learning")

        # Automatic training checkbox
        elif 35 > mouse_position[0] > 10 and 275 > mouse_position[1] > 250:
            self.main_surface.blit(check_mark, (10, 250))
            self.main_surface.fill(CommonSurface.GREY, (211, 251, 23, 23))
            self.trainer = RandomBot("RandomBot")

        # Self-training checkbox
        elif 235 > mouse_position[0] > 210 and 275 > mouse_position[1] > 250:
            self.main_surface.blit(check_mark, (210, 250))
            self.main_surface.fill(CommonSurface.GREY, (11, 251, 23, 23))
            self.trainer = TDBot("TDClone")
            self.trainer.value_function = self.learner.value_function

        # Load TD-Bot
        elif 590 > mouse_position[0] > 440 and 340 > mouse_position[1] > 300:

            try:
                with open("../trained_bots/td-learning.pkl", "rb") as file:
                    td_bot = pickle.load(file)

                self.game_controller = GameController(players=[td_bot, Human("Human")], shape=3,
                                                      number_of_games=1)
                self.current_screen = class_to_switch[1].generate_surface(self.game_controller)

            except FileNotFoundError:
                self.main_surface.fill(CommonSurface.GREY, (440, 300, 150, 40))
                pygame.draw.rect(self.main_surface, CommonSurface.WHITE, (440, 300, 150, 40))
                load_td_bot_button = self.font_small.render("Cannot load !", False, CommonSurface.RED)
                self.main_surface.blit(load_td_bot_button, (470, 310))

        # Train AI button
        elif 590 > mouse_position[0] > 440 and 390 > mouse_position[1] > 350:
            self.game_controller = GameController(players=[self.learner, self.trainer], shape=3,
                                                  number_of_games=200_000)
            self.current_screen = class_to_switch[0].generate_surface(self.game_controller)

        return self.current_screen
