from abc import ABC, abstractmethod
from typing import List

from . import Model


class RandomizableModel(Model, ABC):
    '''the Randomizable model specialization'''
    _precedence: List[str] = []

    @abstractmethod
    def randomize(self) -> None:
        '''randomizes applicable properties values with precedence
constraints'''
        raise NotImplementedError('Randomizable models should implement ' +
                                  "the 'randomize' method")
