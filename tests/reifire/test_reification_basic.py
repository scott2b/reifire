import os
import unittest
from unittest.mock import patch, MagicMock
from reifire.reification import reify

class TestReificationBasic(unittest.TestCase):
    def test_reify_structure(self):
        """Test that reify returns the expected structure."""
        prompt = "test prompt"
        result = reify(prompt)
        
        self.assertIn("object", result)
        self.assertIn("type", result)
        self.assertIn("artifact", result)
        self.assertIn("metadata", result)
        
        self.assertEqual(result["object"]["name"], prompt)
        self.assertEqual(result["metadata"]["original_prompt"], prompt)

    @patch.dict(os.environ, {"NOUNPROJECT_API_KEY": "fake_key", "NOUNPROJECT_API_SECRET": "fake_secret"})
    @patch("reifire.visualization.nounproject.NounProjectClient")
    def test_reify_with_noun_project(self, MockClient):
        """Test reify with Noun Project integration."""
        # Setup mock
        mock_instance = MockClient.return_value
        mock_instance.search_icons.return_value = {
            "icons": [
                {
                    "id": "123",
                    "term": "test",
                    "preview_url": "http://example.com/icon.png",
                    "uploader": {"name": "Tester"}
                }
            ]
        }
        
        prompt = "test"
        result = reify(prompt)
        
        # Verify Noun Project client was initialized and called
        MockClient.assert_called_with("fake_key", "fake_secret")
        mock_instance.search_icons.assert_called_with(prompt, limit=1)
        
        # Verify visualization data
        self.assertIsNotNone(result["artifact"]["visualization"])
        self.assertEqual(result["artifact"]["visualization"]["source"], "nounproject")
        self.assertEqual(result["artifact"]["visualization"]["image"], "http://example.com/icon.png")

    def test_reify_no_credentials(self):
        """Test reify without API credentials."""
        # Ensure no keys in env
        with patch.dict(os.environ, {}, clear=True):
            prompt = "test"
            result = reify(prompt)
            
            self.assertIsNone(result["artifact"]["visualization"])

if __name__ == "__main__":
    unittest.main()
