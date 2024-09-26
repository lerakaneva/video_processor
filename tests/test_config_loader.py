import unittest
from unittest.mock import patch, mock_open
import json
from video_processor.config_loader import ConfigLoader

class TestConfigLoader(unittest.TestCase):
    
    def setUp(self):
        self.valid_config = {
            "output_dir": "/path/to/output",
            "mask_colors": {
                "1": [255, 0, 127],
                "2": [0, 128, 0]
            },
            "alpha": 0.3,
            "chunk_size": 1000
        }
        self.config_loader = None
    
    @patch("builtins.open", new_callable=mock_open, read_data='{"output_dir": "/path/to/output"}')
    def test_valid_config(self, mock_file):
        """Test if ConfigLoader correctly reads a valid config file."""
        self.config_loader = ConfigLoader("dummy_path.json")
        self.assertEqual(self.config_loader.get("output_dir"), "/path/to/output")
    
    @patch("builtins.open", new_callable=mock_open)
    def test_load_full_config(self, mock_file):
        """Test loading config."""
        mock_file.return_value.read.return_value = json.dumps(self.valid_config)
        self.config_loader = ConfigLoader("dummy_path.json")
        self.assertEqual(self.config_loader.get("alpha"), 0.3)
        self.assertEqual(self.config_loader.get("mask_colors")["1"], [255, 0, 127])
    
    @patch("builtins.open", new_callable=mock_open, read_data='{"output_dir": "/path/to/output"}')
    def test_missing_key_with_default(self, mock_file):
        """Test that default values are returned when a key is missing."""
        self.config_loader = ConfigLoader("dummy_path.json")
        # 'alpha' is not in the config, should return the default value
        self.assertEqual(self.config_loader.get("alpha", 0.5), 0.5)
    
    @patch("builtins.open", new_callable=mock_open, read_data='Invalid JSON')
    def test_invalid_json(self, mock_file):
        """Test if ConfigLoader raises an error on invalid JSON."""
        with self.assertRaises(json.JSONDecodeError):
            self.config_loader = ConfigLoader("dummy_path.json")

    @patch("builtins.open", new_callable=mock_open)
    def test_get_method_with_default(self, mock_file):
        """Test the get method with and without a default value."""
        mock_file.return_value.read.return_value = json.dumps(self.valid_config)
        self.config_loader = ConfigLoader("dummy_path.json")
        self.assertEqual(self.config_loader.get("chunk_size"), 1000)
        self.assertEqual(self.config_loader.get("non_existent_key", "default"), "default")

if __name__ == "__main__":
    unittest.main()