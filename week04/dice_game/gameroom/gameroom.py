from iconservice import *


class GameRoom:

    def __init__(self, owner: Address, game_room_id: Address, creation_time: int, participants: list = None, active: bool = False):
        self.owner = owner
        self.game_room_id = game_room_id
        self.creation_time = creation_time
        if participants is None:
            self.participants = []
        else:
            self.participants = participants
        self.active = active

    def join(self, participant: Address):
        self.participants.append(str(participant))

    def escape(self, participant_to_escape: Address):
        self.participants.remove(str(participant_to_escape))

    def game_start(self):
        self.active = True

    def game_stop(self):
        self.active = False

    def __str__(self):
        response = {
            'owner': f'{self.owner}',
            'game_room_id': f'{self.game_room_id}',
            'creation_time': self.creation_time,
            'participants': self.participants,
            'active': self.active
        }
        return json_dumps(response)
