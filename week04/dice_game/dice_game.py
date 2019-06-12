from iconservice import *
from .gameroom.gameroom import GameRoom
from .hand.hand import Hand

TAG = 'DiceGame'

class DiceGame(IconScoreBase):
    _TOKEN_ADDRESS = "token_address"
    _GAME_ROOM = "game_room"
    _GAME_ROOM_LIST = "game_room_list"
    _IN_GAME_ROOM = "in_game_room"
    _HAND = "hand"
    _RESULTS = "results"

    _READY = "ready"
    _GAME_START_TIME = "game_start_time"

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._db = db
        self._DDB_game_room = DictDB(self._GAME_ROOM, db, value_type=str)
        self._DDB_game_start_time = DictDB(self._GAME_START_TIME, db, value_type=int)
        self._DDB_in_game_room = DictDB(self._IN_GAME_ROOM, db, value_type=Address)
        self._DDB_hand = DictDB(self._HAND, db, value_type=str)
        self._DDB_ready = DictDB(self._READY, db, value_type=bool)

    @property
    def game_room_list(self):
        return ArrayDB(self._GAME_ROOM_LIST, self._db, value_type=str)

    @property
    def results(self):
        return ArrayDB(self._RESULTS, self._db, value_type=str)

    @external(readonly=True)
    def showGameRoomList(self) -> list:
        response = []
        game_room_list = self.game_room_list

        for game_room in game_room_list:
            game_room_dict = json_loads(game_room)
            game_room_id = game_room_dict['game_room_id']
            creation_time = game_room_dict['creation_time']
            participants = game_room_dict['participants']
            room_has_vacant_seat = "is Full" if len(participants) > 1 else "has a vacant seat"
            response.append(f"{game_room_id} : ({len(participants)} / 2). The room {room_has_vacant_seat}. Creation time : {creation_time}")

        return response


    @external(readonly=True)
    def getGameRoomStatus(self, _gameroomId: Address) -> dict:
        gameroom_dict = json_loads(self._DDB_game_room[_gameroomId])
        active = "active" if gameroom_dict["active"] else "inactive"

        participants = gameroom_dict["participants"]
        user_ready_status = [participant + " : " + str(self._DDB_ready[Address.from_string(participant)]) for participant in
                             participants]

        response = {
            "status": active,
            "user_ready_status": user_ready_status
        }
        return response

    @external(readonly=True)
    def getUserStatus(self, _userId: Address) -> Address:
        return self._DDB_in_game_room[_userId]

    @external
    def createRoom(self):
        if self._DDB_in_game_room[self.msg.sender] is not None:
            revert("You already joined to another room")


        game_room = GameRoom(self.msg.sender, self.msg.sender, self.block.height)
        game_room.join(self.msg.sender)
        self._DDB_game_room[self.msg.sender] = str(game_room)

        game_room_list = self.game_room_list
        game_room_list.put(str(game_room))
        self._DDB_in_game_room[self.msg.sender] = self.msg.sender

        # Initialize the deck of participant
        new_hand = Hand()
        self._DDB_hand[self.msg.sender] = str(new_hand)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()

    def _get_random(self):
        input_data = f'{self.block.timestamp}'.encode()
        hash = sha3_256(input_data)
        return int.from_bytes(hash, 'big')

    def diceRoll(self) -> int:
        return self._get_random() % 6 +1

    @external
    def joinRoom(self, _gameRoomId: Address):
        # Check whether the game room with game_room_id is existent or not
        if self._DDB_game_room[_gameRoomId] is "":
            revert(f"There is no game room which has equivalent id to {_gameRoomId}")

        # Check the participant is already joined to another game_room
        if self._DDB_in_game_room[self.msg.sender] is not None:
            revert(f"You already joined to another game room : {self._DDB_in_game_room[self.msg.sender]}")

        game_room_dict = json_loads(self._DDB_game_room[_gameRoomId])
        game_room = GameRoom(Address.from_string(game_room_dict['owner']),
                             Address.from_string(game_room_dict['game_room_id']), game_room_dict['creation_time'],
                             game_room_dict['participants'], game_room_dict['active'])
        game_room_list = self.game_room_list


        if len(game_room.participants) > 1:
            revert(f"Full : Can not join to game room {_gameRoomId}")

        # Get in to the game room
        game_room.join(self.msg.sender)
        self._DDB_in_game_room[self.msg.sender] = _gameRoomId
        self._DDB_game_room[_gameRoomId] = str(game_room)

        game_room_index_gen = (index for index in range(len(game_room_list)) if game_room.game_room_id == Address.from_string(json_loads(game_room_list[index])['game_room_id']))

        try:
            index = next(game_room_index_gen)
            game_room_list[index] = str(game_room)
        except StopIteration:
            pass

        new_hand = Hand()
        self._DDB_hand[self.msg.sender] = str(new_hand)

    @external
    def toggleReady(self):
        if self._DDB_in_game_room[self.msg.sender] is None:
            revert("Enter the game room first.")
        if self._DDB_ready[self.msg.sender]:
            self._DDB_ready[self.msg.sender] = False
        else:
            self._DDB_ready[self.msg.sender] = True

    @external
    def gameStart(self):
        game_room_id = self._DDB_in_game_room[self.msg.sender]
        game_room_dict = json_loads(self._DDB_game_room[game_room_id])
        game_room = GameRoom(Address.from_string(game_room_dict['owner']),
                             Address.from_string(game_room_dict['game_room_id']), game_room_dict['creation_time'],
                             game_room_dict['participants'], game_room_dict['active'])
        participants = game_room.participants

        # Check the 'self.msg.sender' == game_room.owner
        if not self.msg.sender == game_room.owner:
            revert("Only owner of game room can start the game")

        if game_room.active:
            revert("The last game is still active and not finalized")

        # Check the number of participants
        if len(participants) < 2:
            revert("Please wait for a challenger to come")

        # Make sure that all the participants are ready
        for participant in participants:
            if not self._DDB_ready[Address.from_string(participant)]:
                revert(f"{participant} is not ready to play game")

        # Game start
        game_room.game_start()
        self._DDB_game_start_time[game_room_id] = self.block.height
        self._DDB_game_room[game_room_id] = str(game_room)

        # Set ready status of both participants to False after starting the game
        for participant in participants:
            self._DDB_ready[Address.from_string(participant)] = False

    @external(readonly=True)
    def showMine(self, _from: Address) -> str:
        hand = self._DDB_hand[_from]
        return hand

    @external
    def hit(self):
        game_room_id = self._DDB_in_game_room[self.msg.sender]
        if game_room_id is None:
            revert("You are not in game")

        game_room_dict = json_loads(self._DDB_game_room[game_room_id])
        game_room = GameRoom(Address.from_string(game_room_dict['owner']),
                             Address.from_string(game_room_dict['game_room_id']), game_room_dict['creation_time'],
                             game_room_dict['participants'], game_room_dict['active'])

        if not game_room.active:
            revert("The game is now in inactive mode")

        hand_dict = json_loads(self._DDB_hand[self.msg.sender])
        hand = Hand(hand_dict['dice'])

        if hand.diceNumber != 0:
            revert('You already fixed your hand')

        hand.assign_dice_number(self.diceRoll())

        self._DDB_hand[self.msg.sender] = str(hand)
