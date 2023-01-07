from abc import ABC
from abc import abstractmethod


class ServerState(ABC):
    def __init__(self, model):
        self.model = model

    # @abstractmethod
    # def enter(self):
    #     pass

    @abstractmethod
    def receive(self, frame):
        pass
