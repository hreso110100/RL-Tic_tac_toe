from abc import ABCMeta, abstractmethod

from src.game import GameController


class CommonPlayer(metaclass=ABCMeta):

    def __init__(self, name, alpha=0.2, gamma=0.8, epsilon=0.9, initial_values=0.5):
        self.name = name
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.initial_values = initial_values
        self.reward = None
        self.action = None

    @abstractmethod
    def mark(self, game: GameController) -> tuple:
        pass

    @abstractmethod
    def update(self, s: str, s_: str, game: GameController):
        pass

    @abstractmethod
    def get_estimates(self, *args) -> float:
        pass

    @abstractmethod
    def print_estimates(self, game: GameController):
        pass
