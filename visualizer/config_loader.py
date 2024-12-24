import json

class ConfigLoader:
    def __init__(self, config_path):
        self.config = self._read_config(config_path)

    def _read_config(self, json_config_path):
        """Reads the JSON configuration file and returns config data."""
        with open(json_config_path, 'r') as f:
            return json.load(f)

    def get(self, key, default=None):
        """Retrieve a configuration value with optional default."""
        return self.config.get(key, default)
