import unittest
from unittest.mock import patch, mock_open
import json
from visualizer.config_loader import ConfigLoader

class TestConfigLoader(unittest.TestCase):
    """
    Tests for the ConfigLoader class.

    This test suite verifies that the ConfigLoader correctly reads and parses JSON
    configuration files, handles missing keys, and raises appropriate errors for
    invalid JSON input.
    """
    def setUp(self):
        """Sets up a valid configuration for testing."""
        self.valid_config = {
            "output_dir": "/path/to/output",
            "mask_colors": {
                "1": [255, 0, 127],
                "2": [0, 128, 0]
            },
            "alpha": 0.3,
            "chunk_size": 1000,
            "cell_labels": [  # Added cell_labels to valid config
                {
                    "name": "test_label",
                    "file": "test_labels.csv",
                    "color": [255, 255, 255]
                 }
             ],
            "cell_trajectories": {
                "file": "trajectories.csv",
                "color": [200, 200, 200]
             },
              "metadata": {
                "pixel_size": 0.22,
                "time_between_frames": 0.1
             }

        }
        self.config_loader = None

    @patch("builtins.open", new_callable=mock_open, read_data='{"output_dir": "/path/to/output"}')
    def test_valid_config(self, mock_file):
        """
        Tests loading a valid configuration file.

        Verifies that the `get` method retrieves the correct value for an existing key.
        """
        self.config_loader = ConfigLoader("dummy_path.json")
        self.assertEqual(self.config_loader.get("output_dir"), "/path/to/output")

    @patch("builtins.open", new_callable=mock_open)
    def test_load_full_config(self, mock_file):
        """
        Test loading a full, complex configuration.

        Checks if all the keys and their corresponding complex values (list, dictionaries)
        are loaded correctly from a larger example config.
        """
        mock_file.return_value.read.return_value = json.dumps(self.valid_config)
        self.config_loader = ConfigLoader("dummy_path.json")
        self.assertEqual(self.config_loader.get("alpha"), 0.3)
        self.assertEqual(self.config_loader.get("mask_colors")["1"], [255, 0, 127])
        self.assertEqual(self.config_loader.get("cell_labels")[0]["name"], "test_label") # Check added field
        self.assertEqual(self.config_loader.get("cell_trajectories")["color"], [200, 200, 200]) # Check added field
        self.assertEqual(self.config_loader.get("metadata")["pixel_size"], 0.22) # Check added field

    @patch("builtins.open", new_callable=mock_open, read_data='{"output_dir": "/path/to/output"}')
    def test_missing_key_with_default(self, mock_file):
        """
        Tests retrieving a missing key with a default value.
        """
        self.config_loader = ConfigLoader("dummy_path.json")
        self.assertEqual(self.config_loader.get("alpha", 0.5), 0.5)  # 'alpha' is missing

    @patch("builtins.open", new_callable=mock_open, read_data='Invalid JSON')
    def test_invalid_json(self, mock_file):
        """
        Tests handling invalid JSON input.

        Verifies that a JSONDecodeError is raised when attempting to load a malformed
        JSON configuration file.
        """
        with self.assertRaises(json.JSONDecodeError):
            self.config_loader = ConfigLoader("dummy_path.json")

    @patch("builtins.open", new_callable=mock_open)
    def test_get_method_with_default(self, mock_file):
        """Test get method with and without a default value"""

        mock_file.return_value.read.return_value = json.dumps(self.valid_config)
        self.config_loader = ConfigLoader("dummy_path.json")
        self.assertEqual(self.config_loader.get("chunk_size"), 1000)
        self.assertIsNone(self.config_loader.get("non_existent_key")) # Check if nothing is returned
        self.assertEqual(self.config_loader.get("non_existent_key", "default"), "default")

if __name__ == "__main__":
    unittest.main()
