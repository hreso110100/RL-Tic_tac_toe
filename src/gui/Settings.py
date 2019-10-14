import pickle

import pygame

from src.game.GameController import GameController
from src.game.TextInput import TextInput
from src.gui.CommonSurface import CommonSurface
from src.players.agents.ApproximateQBot import ApproximateQBot
from src.players.agents.NeuralNetworkBot import NeuralNetworkBot
from src.players.agents.QBot import QBot
from src.players.agents.SarsaBot import SarsaBot
from src.players.agents.TDBot import TDBot
from src.players.opponents.Human import Human
from src.players.opponents.RandomBot import RandomBot


class Settings(CommonSurface):
    learner = None
    trainer = None
    game_controller = None
    active = 0

    def __init__(self, main_surface):
        self.board_shape = 0
        self.iterations = 0
        self.text_input_iterations = TextInput()
        self.text_input_board_size = TextInput()
        super().__init__(main_surface)

    def generate_surface(self, game_controller=None) -> str:
        self.clear_surface()
        self.current_screen = "SETTINGS"

        choose_board_size_text = self.font_medium.render("Enter board size", False, CommonSurface.BLUE)
        self.main_surface.blit(choose_board_size_text, (10, 10))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [10, 49, 210, 45], 1)

        choose_board_size_text = self.font_medium.render("Enter number of iterations", False, CommonSurface.BLUE)
        self.main_surface.blit(choose_board_size_text, (280, 10))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [279, 49, 310, 45], 1)

        select_algorithm_text = self.font_medium.render("Select AI algorithm", False, CommonSurface.BLUE)
        self.main_surface.blit(select_algorithm_text, (10, 100))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [10, 150, 25, 25], 1)
        q_learning_text = self.font_medium.render("TD(0)", False, CommonSurface.WHITE)
        self.main_surface.blit(q_learning_text, (50, 145))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [10, 200, 25, 25], 1)
        q_learning_text = self.font_medium.render("SARSA", False, CommonSurface.WHITE)
        self.main_surface.blit(q_learning_text, (50, 195))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [210, 150, 25, 25], 1)
        sarsa_text = self.font_medium.render("Q-learning", False, CommonSurface.WHITE)
        self.main_surface.blit(sarsa_text, (250, 145))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [410, 150, 25, 25], 1)
        td_learning_text = self.font_medium.render("DQN", False, CommonSurface.WHITE)
        self.main_surface.blit(td_learning_text, (450, 145))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [210, 200, 25, 25], 1)
        td_learning_text = self.font_medium.render("Approximate Q-learning", False, CommonSurface.WHITE)
        self.main_surface.blit(td_learning_text, (250, 195))

        choose_train_method_text = self.font_medium.render("Choose how to train ", False, CommonSurface.BLUE)
        self.main_surface.blit(choose_train_method_text, (10, 235))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [10, 285, 25, 25], 1)
        random_training_text = self.font_medium.render("Random", False, CommonSurface.WHITE)
        self.main_surface.blit(random_training_text, (50, 280))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [210, 285, 25, 25], 1)
        clone_training_text = self.font_medium.render("Clone", False, CommonSurface.WHITE)
        self.main_surface.blit(clone_training_text, (250, 285))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [410, 285, 25, 25], 1)
        clone_training_text = self.font_medium.render("Human", False, CommonSurface.WHITE)
        self.main_surface.blit(clone_training_text, (450, 285))

        pygame.draw.rect(self.main_surface, CommonSurface.BLUE, (300, 350, 130, 40))
        load_q_bot_button = self.font_small.render("Load AI", False, CommonSurface.WHITE)
        self.main_surface.blit(load_q_bot_button, (330, 360))

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, (460, 350, 130, 40))
        train_button = self.font_small.render("Train AI", False, CommonSurface.BLUE)
        self.main_surface.blit(train_button, (490, 360))

        return self.current_screen

    def handle_typing(self, events, mouse_position):

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [279, 49, 310, 45], 1)
        pygame.draw.rect(self.main_surface, CommonSurface.GREY, [280, 50, 300, 40])

        pygame.draw.rect(self.main_surface, CommonSurface.WHITE, [10, 49, 210, 45], 1)
        pygame.draw.rect(self.main_surface, CommonSurface.GREY, [11, 50, 200, 40])

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 589 > mouse_position[0] > 279 and 94 > mouse_position[1] > 49:
                    self.active = 1

                elif 220 > mouse_position[0] > 10 and 94 > mouse_position[1] > 49:
                    self.active = 2

        if self.active == 1:
            self.text_input_iterations.update(events)

            if 0 < len(self.text_input_iterations.get_text()) <= 15:
                self.iterations = int(self.text_input_iterations.get_text())
            else:
                self.iterations = 0

        elif self.active == 2:
            self.text_input_board_size.update(events)

            if 0 < len(self.text_input_board_size.get_text()) <= 2:
                self.board_shape = int(self.text_input_board_size.get_text())
            else:
                self.board_shape = 0

        self.main_surface.blit(self.text_input_iterations.get_surface(), (283, 55))
        self.main_surface.blit(self.text_input_board_size.get_surface(), (14, 55))

    def handle_clicks(self, mouse_position, class_to_switch) -> str:
        check_mark = pygame.image.load('../assets/check_mark.png')
        check_mark = pygame.transform.scale(check_mark, (25, 25))

        # Q-learning checkbox
        if 235 > mouse_position[0] > 210 and 175 > mouse_position[1] > 150:
            self.main_surface.blit(check_mark, (210, 150))
            self.main_surface.fill(CommonSurface.GREY, (11, 201, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (11, 151, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (211, 201, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (411, 151, 23, 23))
            self.learner = QBot("Q-learning")

        # SARSA checkbox
        elif 35 > mouse_position[0] > 10 and 225 > mouse_position[1] > 200:
            self.main_surface.blit(check_mark, (10, 200))
            self.main_surface.fill(CommonSurface.GREY, (211, 151, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (11, 151, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (211, 201, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (411, 151, 23, 23))
            self.learner = SarsaBot("SARSA")

        # TD learning checkbox
        elif 35 > mouse_position[0] > 10 and 175 > mouse_position[1] > 150:
            self.main_surface.blit(check_mark, (10, 150))
            self.main_surface.fill(CommonSurface.GREY, (11, 201, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (211, 151, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (211, 201, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (411, 151, 23, 23))
            self.learner = TDBot("TD(0)")

        # Approximate Q-learning
        elif 235 > mouse_position[0] > 210 and 235 > mouse_position[1] > 200:
            self.main_surface.blit(check_mark, (210, 200))
            self.main_surface.fill(CommonSurface.GREY, (11, 151, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (11, 201, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (211, 151, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (411, 151, 23, 23))
            self.learner = ApproximateQBot("Approximate Q")

        # DQN checkbox
        elif 435 > mouse_position[0] > 410 and 185 > mouse_position[1] > 150:
            self.main_surface.blit(check_mark, (410, 150))
            self.main_surface.fill(CommonSurface.GREY, (11, 151, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (11, 201, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (211, 201, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (211, 151, 23, 23))
            self.learner = NeuralNetworkBot("DQN")

        # Random opponent training checkbox
        elif 35 > mouse_position[0] > 10 and 310 > mouse_position[1] > 285:
            self.main_surface.blit(check_mark, (10, 285))
            self.main_surface.fill(CommonSurface.GREY, (211, 286, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (411, 286, 23, 23))
            self.trainer = RandomBot("RandomBot")

        # Self-training checkbox
        elif 235 > mouse_position[0] > 210 and 310 > mouse_position[1] > 285:
            self.main_surface.blit(check_mark, (210, 285))
            self.main_surface.fill(CommonSurface.GREY, (11, 286, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (411, 286, 23, 23))

            if type(self.learner) is QBot:
                self.trainer = QBot("Clone")
                self.trainer.q_function = self.learner.q_function
            elif type(self.learner) is TDBot:
                self.trainer = TDBot("Clone")
                self.trainer.value_function = self.learner.value_function
            elif type(self.learner) is SarsaBot:
                self.trainer = SarsaBot("Clone")
                self.trainer.q_function = self.learner.q_function
            elif type(self.learner) is ApproximateQBot:
                self.trainer = ApproximateQBot("Clone")
                self.trainer.features_weights = self.learner.features_weights
            elif type(self.learner) is NeuralNetworkBot:
                self.trainer = NeuralNetworkBot("Clone")

        # Human opponent training checkbox
        elif 435 > mouse_position[0] > 410 and 310 > mouse_position[1] > 285:
            self.main_surface.blit(check_mark, (410, 285))
            self.main_surface.fill(CommonSurface.GREY, (11, 286, 23, 23))
            self.main_surface.fill(CommonSurface.GREY, (211, 286, 23, 23))
            self.trainer = Human("Human")

        # Load AI button
        elif 430 > mouse_position[0] > 300 and 390 > mouse_position[1] > 350:

            try:
                with open(f"../trained_bots/{self.learner.name}.pkl", "rb") as file:
                    bot = pickle.load(file)

                if type(self.trainer) is Human:
                    self.game_controller = GameController(players=[bot, self.trainer], shape=self.board_shape,
                                                          number_of_games=1)
                    self.current_screen = class_to_switch[1].generate_surface(self.game_controller)
                else:
                    self.game_controller = GameController(players=[bot, self.trainer], shape=self.board_shape,
                                                          number_of_games=self.iterations)
                    # TODO remove
                    self.game_controller.players[0].epsilon = 0
                    self.current_screen = class_to_switch[0].generate_surface(self.game_controller)

            except FileNotFoundError:
                self.main_surface.fill(CommonSurface.GREY, (300, 350, 130, 40))
                pygame.draw.rect(self.main_surface, CommonSurface.BLUE, (300, 350, 130, 40))
                load_bot_button = self.font_small.render("Cannot load !", False, CommonSurface.RED)
                self.main_surface.blit(load_bot_button, (320, 360))

        # Train AI button
        elif 590 > mouse_position[0] > 460 and 390 > mouse_position[1] > 350:

            if type(self.trainer) is Human:
                self.game_controller = GameController(players=[self.learner, self.trainer], shape=self.board_shape,
                                                      number_of_games=1)

                if type(self.learner) is NeuralNetworkBot:
                    self.learner.model = self.learner.create_model(self.game_controller)
                    self.learner.target_model = self.learner.create_model(self.game_controller)

                self.current_screen = class_to_switch[1].generate_surface(self.game_controller)

            else:
                self.game_controller = GameController(players=[self.learner, self.trainer], shape=self.board_shape,
                                                      number_of_games=self.iterations)

                if type(self.learner) is NeuralNetworkBot:
                    self.learner.model = self.learner.create_model(self.game_controller)
                    self.learner.target_model = self.learner.create_model(self.game_controller)

                if type(self.trainer) is NeuralNetworkBot:
                    self.trainer.model = self.trainer.create_model(self.game_controller)
                    self.trainer.target_model = self.trainer.create_model(self.game_controller)

                self.current_screen = class_to_switch[0].generate_surface(self.game_controller)

        return self.current_screen
