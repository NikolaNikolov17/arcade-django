from django.test import TestCase
from rest_framework.test import APITestCase

from games.models import Game
from users.models import User


# Create your tests here.
class GameModelTest(TestCase):
    def test_game_creation(self):
        game = Game.objects.create(
            name="Test Game",
            description="This is a test game.",

        )
        self.assertEqual(game.name, "Test Game")


class GameAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='1234')
        self.client.login(username='test', password='1234')
        self.game = Game.objects.create(name='API Game', description='Test description')

    def test_game_list(self):
        response = self.client.get('/api/games/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('API Game', str(response.data))