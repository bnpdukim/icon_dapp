from iconservice import *


values = {'default': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6}


class Hand:
    _DEFAULT_VALUE = 0

    def __init__(self):
        self.diceNumber = self._DEFAULT_VALUE

    def assign_dice_number(self, number: int):
        self.diceNumber = number

    def __str__(self):
        response = {
            'dice': self.diceNumber
        }
        return json_dumps(response)
