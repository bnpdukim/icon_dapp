from iconservice import *

TAG = 'UserInterface'

class SampleInterface(InterfaceScore):
    @interface
    def getOwnerName(self):
        pass

class UserInterface(IconScoreBase):

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()
    
    @external(readonly=True)
    def getOwnerName(self) -> str:
        interface = self.create_interface_score(Address.from_string("cx9236ea48fa98edf78bb4294fd225912d112072a7"), SampleInterface)
        return interface.getOwnerName()
