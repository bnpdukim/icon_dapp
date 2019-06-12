from iconservice import *

TAG = 'DiceGame'

class DiceGame(IconScoreBase):

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._db = db
        self._DDB_hand = DictDB(self._HAND, db, value_type=str)
        self._DDB_ready = DictDB(self._READY, db, value_type=bool)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()

    def _get_random(self, data: str):
        input_data = f'{self.block.timestamp}, {data}'.encode()
        hash = sha3_256(input_data)
        return int.from_bytes(hash, 'big')

    @external(readonly=True)
    def join(self, _from: Address) -> int:


    @external(readonly=True)
    def roll_dice(self, _from: Address) -> int:
        return self._get_random(_from.__hash__()) % 6

    @external(readonly=True)
    def showAndReset(self) -> str:
