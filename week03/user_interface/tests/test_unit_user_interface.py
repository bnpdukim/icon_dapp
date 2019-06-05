from ..user_interface import UserInterface
from tbears.libs.scoretest.score_test_case import ScoreTestCase


class TestUserInterface(ScoreTestCase):

    def setUp(self):
        super().setUp()
        self.score = self.get_score_instance(UserInterface, self.test_account1)

    def test_owner_name(self):
        print(self.score.getOwnerName())
