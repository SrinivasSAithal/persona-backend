from django.test import TestCase
from rest_framework.test import APIClient

from media_tracker.models import Media


class MediaProgressStatusTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.media = Media.objects.create(
            title="Test Anime",
            current_season=2,
            current_episode=5,
            status=Media.StatusChoices.COMPLETED,
        )

    def test_increment_episode_switches_to_watching(self):
        response = self.client.patch(f"/api/media/{self.media.id}/episode/increment/", {}, format="json")

        self.assertEqual(response.status_code, 200)
        self.media.refresh_from_db()
        self.assertEqual(self.media.current_episode, 6)
        self.assertEqual(self.media.status, Media.StatusChoices.WATCHING)

    def test_decrement_episode_switches_to_watching(self):
        response = self.client.patch(f"/api/media/{self.media.id}/episode/decrement/", {}, format="json")

        self.assertEqual(response.status_code, 200)
        self.media.refresh_from_db()
        self.assertEqual(self.media.current_episode, 4)
        self.assertEqual(self.media.status, Media.StatusChoices.WATCHING)

    def test_decrement_season_switches_to_watching(self):
        response = self.client.patch(f"/api/media/{self.media.id}/season/decrement/", {}, format="json")

        self.assertEqual(response.status_code, 200)
        self.media.refresh_from_db()
        self.assertEqual(self.media.current_season, 1)
        self.assertEqual(self.media.current_episode, 0)
        self.assertEqual(self.media.status, Media.StatusChoices.WATCHING)

    def test_editing_progress_switches_to_watching(self):
        response = self.client.patch(
            f"/api/media/{self.media.id}/",
            {
                "title": "Test Anime",
                "current_season": 3,
                "current_episode": 1,
                "status": Media.StatusChoices.DROPPED,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.media.refresh_from_db()
        self.assertEqual(self.media.current_season, 3)
        self.assertEqual(self.media.current_episode, 1)
        self.assertEqual(self.media.status, Media.StatusChoices.WATCHING)

    def test_can_store_zero_progress_values(self):
        media = Media.objects.create(title="Zero Start Anime")

        self.assertEqual(media.current_season, 0)
        self.assertEqual(media.current_episode, 0)