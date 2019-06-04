from iconservice import *

TAG = 'SampleOne'

class SampleOne(IconScoreBase):
    _OWNER_NAME = "owner_name"

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._owner_name = VarDB(self._OWNER_NAME, db, str)

    def on_install(self) -> None:
        super().on_install()
        self._owner_name.set("Life4honor")

    def on_update(self) -> None:
        super().on_update()

    @external(readonly=True)
    def hello(self) -> str:
        return f"Hello {self._owner_name.get()}"
