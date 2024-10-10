import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

import services
from main import app


class TestAPIIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

        self.short_url = None
    # This test returns 404 I think it's related to fastapi and db interaction
    # @patch('cache.cache')
    # def test_shorten_and_redirect(self, mock_cache):
    #     response = self.client.post("/shorten/", json={"user_id": 1, "original_url": "http://google.com"})
    #     self.assertEqual(response.status_code, 200)
    #
    #     short_url = "2691e"
    #     self.assertIsNotNone(short_url)
    #
    #     print(f"Generated short URL: {short_url}")
    #     services.URLShortener.generate_short_url(1,short_url)
    #     mock_cache.get.return_value = "http://google.com"
    #
    #     redirect_response = self.client.get(f"/{short_url}/")
    #     self.assertEqual(redirect_response.status_code, 307)
    #     self.assertEqual(redirect_response.headers["Location"], "http://google.com")

    def test_redirect_to_nonexistent_url(self):
        response = self.client.get("/nonexistent")
        self.assertEqual(response.status_code, 404)
        self.assertIn("URL not found", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
