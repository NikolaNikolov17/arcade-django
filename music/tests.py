from django.test import TestCase
from rest_framework.test import APITestCase

from music.models import Song
from users.models import User


# Create your tests here.
class SongModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='1234')

    def test_song_creation(self):
        song = Song.objects.create(
            title="Test Song",
            youtube_url="http://test.com/song",
            added_by=self.user
        )
        self.assertEqual(song.title, "Test Song")
        self.assertTrue(song.youtube_url.startswith("http://"))


class SongAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='1234')
        self.client.login(username='test', password='1234')
        self.song = Song.objects.create(title='API Song', youtube_url='http://test.com/song', added_by=self.user)

    def test_song_list(self):
        response = self.client.get('/api/music/songs/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('API Song', str(response.data))