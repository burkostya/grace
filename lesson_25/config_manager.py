# FILE:lesson_25/config_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Handles persistent configuration for Lesson 25 in config.json.
# SCOPE:Reading and writing dictionary-based config to disk.
# INPUT:Dictionary of parameters (a, c, x_min, x_max).
# OUTPUT:Dictionary of parameters.
# KEYWORDS:[DOMAIN(8):Configuration; CONCEPT(7):Persistence; TECH(9):JSON]
# LINKS:[READS_DATA_FROM(9):lesson_25/config.json]
# END_MODULE_CONTRACT

# START_RATIONALE:
# Q: Why use a class instead of simple functions?
# A: Encapsulation of the file path and potential for adding validation or default logic in one place.
# END_RATIONALE

# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Initial implementation of ConfigManager.]
# END_CHANGE_SUMMARY

# START_MODULE_MAP:
# CLASS 10[Manages reading and writing config.json] => ConfigManager
# END_MODULE_MAP

import json
import os
import logging

logger = logging.getLogger(__name__)


# START_FUNCTION_ConfigManager
class ConfigManager:
    """
    ConfigManager handles the lifecycle of the config.json file.
    It provides methods to load existing configuration or return defaults if the file is missing,
    and to save updated parameters back to the file.
    """

    def __init__(self, config_path="lesson_25/config.json"):
        self.config_path = config_path
        self.default_config = {"a": 1.0, "c": 0.0, "x_min": -10.0, "x_max": 10.0}
        logger.debug(
            f"[Config][IMP:4][ConfigManager][init][Flow] Initialized with path: {self.config_path}"
        )

    # START_FUNCTION_load_config
    # START_CONTRACT:
    # PURPOSE:Loads configuration from JSON file or returns defaults.
    # INPUTS: None
    # OUTPUTS: - dict - configuration parameters.
    # SIDE_EFFECTS: None
    # COMPLEXITY_SCORE: 3
    # END_CONTRACT
    def load_config(self) -> dict:
        """
        Reads config.json from disk. If the file is missing or malformed, returns default values.
        """
        # START_BLOCK_READ_FILE: [Reading file content]
        if not os.path.exists(self.config_path):
            logger.info(
                f"[BeliefState][IMP:9][ConfigManager][load_config][Condition] Config file not found. Using defaults. [VALUE]"
            )
            return self.default_config

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.debug(
                    f"[Config][IMP:7][ConfigManager][load_config][IO] Successfully loaded config from {self.config_path}"
                )
                return data
        except (json.JSONDecodeError, IOError) as e:
            logger.critical(
                f"[SystemError][IMP:10][ConfigManager][load_config][Exception] Failed to read config: {e}. Falling back to defaults."
            )
            return self.default_config
        # END_BLOCK_READ_FILE

    # END_FUNCTION_load_config

    # START_FUNCTION_save_config
    # START_CONTRACT:
    # PURPOSE:Saves configuration to JSON file.
    # INPUTS: - dict => config: configuration dictionary.
    # OUTPUTS: - bool - success status.
    # SIDE_EFFECTS: Overwrites config.json
    # COMPLEXITY_SCORE: 3
    # END_CONTRACT
    def save_config(self, config: dict) -> bool:
        """
        Writes the provided configuration dictionary to config.json in a pretty-printed format.
        """
        # START_BLOCK_WRITE_FILE: [Writing file content]
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            logger.info(
                f"[BeliefState][IMP:9][ConfigManager][save_config][IO] Saved config to {self.config_path}. [SUCCESS]"
            )
            return True
        except IOError as e:
            logger.critical(
                f"[SystemError][IMP:10][ConfigManager][save_config][Exception] Failed to save config: {e}"
            )
            return False
        # END_BLOCK_WRITE_FILE

    # END_FUNCTION_save_config


# END_FUNCTION_ConfigManager
