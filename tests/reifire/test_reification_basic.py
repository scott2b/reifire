import unittest
from unittest.mock import MagicMock, patch
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

    def test_reify_with_provider_chain(self):
        """Test reify with a mock provider chain."""
        mock_chain = MagicMock()
        mock_chain.search.return_value = [
            {
                "id": "123",
                "name": "test",
                "source": "bundled",
                "image": "data:image/svg+xml;base64,abc",
                "attribution": "",
            }
        ]

        prompt = "test"
        result = reify(prompt, provider_chain=mock_chain)

        mock_chain.search.assert_called()
        self.assertIsNotNone(result["artifact"]["visualization"])
        self.assertEqual(result["artifact"]["visualization"]["source"], "bundled")

    def test_reify_default_chain(self):
        """Test reify with default chain (bundled icons always available)."""
        prompt = "cat"
        result = reify(prompt)

        # With bundled icons, we should get results without any API keys
        # The result should have the basic structure regardless
        self.assertIn("artifact", result)
        self.assertIn("attributes", result["artifact"])


if __name__ == "__main__":
    unittest.main()
