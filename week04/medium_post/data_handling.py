from iconservice import json_dumps


class DataHandlingClass:
    def __init__(self, attr1: int, attr2: str, attr3: bool):
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3

    def __str__(self):
        dict_to_str = {
            'attr1': self.attr1,
            'attr2': self.attr2,
            'attr3': self.attr3
        }
        return json_dumps(dict_to_str)

    def to_str(self):
        dict_to_str = {
            'attr1': self.attr1,
            'attr2': self.attr2,
            'attr3': self.attr3
        }
        return json_dumps(dict_to_str)

    def handle_data(self, attr1: int, attr2: str, attr3: bool):
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3