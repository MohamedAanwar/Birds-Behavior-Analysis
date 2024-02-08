from abc import ABC,abstractmethod
class Producer(ABC):

    @abstractmethod
    def produce(**args):
        pass