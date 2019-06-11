from iconservice import *

TAG = 'UserInterface'

class SampleInterface(InterfaceScore):
    @interface
    def getOwnerName(self):
        pass

class UserInterface(IconScoreBase):
    _INTERFACE_CA = "interface_ca"

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._interface_ca = VarDB(self._INTERFACE_CA, db, value_type=Address)

    def on_install(self, _sampleAddress: Address) -> None:
        super().on_install()
        self._interface_ca.set(_sampleAddress)

    def on_update(self) -> None:
        super().on_update()

    @property
    def sample_address(self):
        return self._interface_ca.get()
    
    @external(readonly=True)
    def ownerName(self) -> str:
        _sampleScore = self.create_interface_score(self.sample_address, SampleInterface)
        return _sampleScore.getOwnerName()
