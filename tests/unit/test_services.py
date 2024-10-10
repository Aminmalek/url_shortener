import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from main import app
from services import URLShortener


class TestURLShortener(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.mock_db = MagicMock()
        self.url_shortener = URLShortener(self.mock_db)

    @patch('cache.cache')  # Replace with your actual cache import
    def test_shorten_url_success(self, mock_cache):
        # Given
        mock_cache.get.return_value = None
        self.mock_db.query.return_value.filter_by.return_value.first.return_value = None

        # When
        response = self.client.post("/shorten/", json={"user_id": 1, "original_url": "http://example.com"})

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertIn("short_url", response.json())

    @patch('cache.cache')
    def test_shorten_url_retry(self, mock_cache):
        # Given
        mock_cache.get.return_value = None
        self.mock_db.query.return_value.filter_by.return_value.first.side_effect = [None, MagicMock(short_url='f5503')]

        response = self.client.post("/shorten/", json={"user_id": 1, "original_url": "http://example.com"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["short_url"], "firouze.shortener.com/f5503")  # Check with the mocked value

    def test_generate_short_url(self):
        user_id = 1
        original_url = "http://example.com"

        short_url = self.url_shortener.generate_short_url(user_id, original_url)

        self.assertEqual(len(short_url), 5)  # Check that the length of the short URL is 5

    def test_create_new_entry(self):
        user_id = 1
        original_url = "http://example.com"
        short_url = "abcde"

        short_url_created = self.url_shortener.create_new_entry(user_id, original_url, short_url)

        self.assertEqual(short_url_created, short_url)
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
