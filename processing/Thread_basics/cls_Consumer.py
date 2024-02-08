from abc import ABC,abstractmethod
class Cosnumer(ABC):

    @abstractmethod
    def consume(**args):
        pass