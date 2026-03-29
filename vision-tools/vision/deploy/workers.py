from abc import abstractmethod


class Worker:
    
    @abstractmethod
    def process(self, images):
        pass
