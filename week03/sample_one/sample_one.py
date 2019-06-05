from iconservice import *

TAG = 'SampleOne'

class SampleOne(IconScoreBase):
    _OWNER_NAME = "owner_name"
    _ARRAY_DB_SAMPLE = "array_db_sample"
    _DICT_DB_SAMPLE = "dict_db_sample"


    @eventlog
    def OwnerNameChanged(self, owner_name:str):
        pass

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._owner_name = VarDB(self._OWNER_NAME, db, str)
        self._dict_db = DictDB(self._DICT_DB_SAMPLE, db, str)

    def on_install(self) -> None:
        super().on_install()
        self._owner_name.set("Life4honor 2")

        self._dict_db["Jin"] = "Developer"
        self._array_db.put("Jin")

        self._dict_db["nanaones"] = "Developer"
        self._array_db.put("nanaones")

        self._dict_db["ICON"] = "Blockchain"
        self._array_db.put("ICON")

        self._dict_db["SCORE"] = "Smart Contract"
        self._array_db.put("SCORE")

    def on_update(self) -> None:
        super().on_update()

    @property
    def _array_db(self):
        return ArrayDB(self._ARRAY_DB_SAMPLE, self.db, str)

    @external(readonly=True)
    def hello(self) -> str:
        owner = self._owner_name.get()
        elements = [(el, self._dict_db[el]) for el in self._array_db]
        return f"{owner} : Owner, {elements}"

    @external
    def setOwnerName(self, owner_name:str):
        self._owner_name.set(owner_name)
        self.OwnerNameChanged(owner_name)

    @external(readonly=True)
    def getOwnerName(self)->str:
        self._owner_name.get()

    @payable
    @external
    def deposit(self):
        pass

    @payable
    def fallback(self):
        if self.msg.value >= 10000000000000000000:
            revert("ICX amount must be lower than 10")
