# FILE:lesson_23/config_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Manages the application configuration in config.json.
# SCOPE:Reading and writing settings (a, c, x_min, x_max).
# INPUT:Dictionary or JSON file path.
# OUTPUT:Configuration dictionary.
# KEYWORDS:DOMAIN(Config): Persistent settings; CONCEPT(State): Global application state.
# LINKS:READS_DATA_FROM(config.json)
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: 1.0.0 - Initial implementation of ConfigManager.
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# CLASS[8][Handles configuration persistence] => ConfigManager
# FUNC[7][Loads configuration from file] => ConfigManager.load_config
# FUNC[7][Saves configuration to file] => ConfigManager.save_config
# END_MODULE_MAP

import json
import os
import logging


# START_FUNCTION_ConfigManager
class ConfigManager:
    """
    Manager for the lesson_23 configuration. Provides thread-safe-ish (simple file I/O)
    loading and saving of simulation parameters to a local config.json.
    """

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.logger = logging.getLogger("app_23")

    # START_FUNCTION_load_config
    # START_CONTRACT:
    # PURPOSE: Loads configuration from JSON file.
    # INPUTS: None
    # OUTPUTS: dict - Configuration parameters.
    # COMPLEXITY_SCORE: 3
    # END_CONTRACT
    def load_config(self) -> dict:
        """
        Loads the config.json file. If it doesn't exist, returns default values.
        """
        # START_BLOCK_FILE_CHECK:[Check if config exists]
        if not os.path.exists(self.config_path):
            defaults = {"a": 1.0, "c": 0.0, "x_min": -10, "x_max": 10}
            self.logger.info(
                f"[INFO][IMP:7][ConfigManager][load_config][FILE_IO] Config not found. Using defaults.[SUCCESS]"
            )
            return defaults
        # END_BLOCK_FILE_CHECK

        # START_BLOCK_READ:[Read JSON from file]
        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)
            self.logger.info(
                f"[INFO][IMP:6][ConfigManager][load_config][FILE_IO] Config loaded successfully.[SUCCESS]"
            )
            return data
        except Exception as e:
            self.logger.error(
                f"[ERROR][IMP:10][ConfigManager][load_config][CRITICAL] Failed to read config: {e}[FAILURE]"
            )
            return {"a": 1.0, "c": 0.0, "x_min": -10, "x_max": 10}
        # END_BLOCK_READ

    # END_FUNCTION_load_config

    # START_FUNCTION_save_config
    # START_CONTRACT:
    # PURPOSE: Saves configuration to JSON file.
    # INPUTS: - data: dict => config dictionary
    # OUTPUTS: bool - Success status.
    # COMPLEXITY_SCORE: 3
    # END_CONTRACT
    def save_config(self, data: dict) -> bool:
        """
        Writes the provided configuration dictionary to config.json.
        """
        # START_BLOCK_WRITE:[Write JSON to file]
        try:
            with open(self.config_path, "w") as f:
                json.dump(data, f, indent=4)
            self.logger.info(
                f"[INFO][IMP:8][ConfigManager][save_config][FILE_IO] Config saved successfully.[SUCCESS]"
            )
            return True
        except Exception as e:
            self.logger.error(
                f"[ERROR][IMP:10][ConfigManager][save_config][CRITICAL] Failed to save config: {e}[FAILURE]"
            )
            return False
        # END_BLOCK_WRITE

    # END_FUNCTION_save_config


# END_FUNCTION_ConfigManager
