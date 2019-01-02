from abc import ABCMeta, abstractmethod


class CommonPlayer(metaclass=ABCMeta):

    def __init__(self, name):
        self.name = name
        self.reward = None

    @abstractmethod
    def mark_grid(self, game_controller) -> tuple:
        pass

    def update_state_value(self, state_to_estimate, state_after_action):
        pass

    def get_state_value(self, state_key) -> float:
        pass
