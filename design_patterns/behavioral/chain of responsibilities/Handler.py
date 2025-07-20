

from abc import ABC, abstractmethod


class Handler(ABC):
    def __init__(self, sucessor = None):
        self.sucessor = sucessor
    
    @abstractmethod
    def handle_request(self, request):
        pass



