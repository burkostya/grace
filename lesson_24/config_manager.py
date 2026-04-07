# FILE:lesson_24/config_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Manage application state by reading and writing config.json.
# SCOPE: State management (a, c, x_min, x_max).
# INPUT: JSON format parameters.
# OUTPUT: Dictionary of parameters.
# KEYWORDS:DOMAIN(Parabola): State; CONCEPT(Config): JSON_IO
# LINKS:READS_DATA_FROM(config.json)
# END_MODULE_CONTRACT
#
# START_RATIONALE:
# Q: Why use a standalone module for config?
# A: To ensure strict layer isolation and single point of truth for state.
# END_RATIONALE
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: 1.0.0 - Initial implementation of config manager.
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC [8][Loads configuration from file] => load_config
# FUNC [8][Saves configuration to file] => save_config
# END_MODULE_MAP

import json
import os
import logging

# START_BLOCK_LOGGING_SETUP: [Setup local logger]
logger = logging.getLogger("lesson_24.config_manager")
# END_BLOCK_LOGGING_SETUP


# START_FUNCTION_load_config
# START_CONTRACT:
# PURPOSE:Read parameters from config.json.
# INPUTS:
# - file_path: str => config file path
# OUTPUTS:
# - dict - Loaded parameters
# SIDE_EFFECTS: None
# KEYWORDS:PATTERN(IO): Reader
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def load_config(file_path="lesson_24/config.json"):
    """
    Reads the configuration file and returns a dictionary of parameters.
    If the file does not exist, it returns default values (a=1, c=0, x_min=-10, x_max=10).
    Uses LDD 2.0 logging to track the belief state about file presence.
    """
    # START_BLOCK_READ:[Perform file read]
    if not os.path.exists(file_path):
        logger.info(
            f"[IMP:9][load_config][READ][IO] File {file_path} not found. Using defaults.[BELIEF:DEFAULT_STATE]"
        )
        return {"a": 1.0, "c": 0.0, "x_min": -10.0, "x_max": 10.0}

    try:
        with open(file_path, "r") as f:
            config = json.load(f)
            logger.info(
                f"[IMP:7][load_config][READ][IO] Configuration loaded from {file_path}.[SUCCESS]"
            )
            return config
    except Exception as e:
        logger.error(
            f"[IMP:10][load_config][READ][ERROR] Failed to read config: {str(e)}[CRITICAL]"
        )
        return {"a": 1.0, "c": 0.0, "x_min": -10.0, "x_max": 10.0}
    # END_BLOCK_READ


# END_FUNCTION_load_config


# START_FUNCTION_save_config
# START_CONTRACT:
# PURPOSE:Write parameters to config.json.
# INPUTS:
# - config: dict => parameters to save
# - file_path: str => config file path
# OUTPUTS:
# - bool - Success status
# SIDE_EFFECTS: Overwrites config.json
# KEYWORDS:PATTERN(IO): Writer
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def save_config(config, file_path="lesson_24/config.json"):
    """
    Writes the provided dictionary to the configuration file in JSON format.
    Ensures the directory exists before writing.
    """
    # START_BLOCK_WRITE:[Perform file write]
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(config, f, indent=4)
        logger.info(
            f"[IMP:8][save_config][WRITE][IO] Configuration saved to {file_path}.[SUCCESS]"
        )
        return True
    except Exception as e:
        logger.error(
            f"[IMP:10][save_config][WRITE][ERROR] Failed to save config: {str(e)}[CRITICAL]"
        )
        return False
    # END_BLOCK_WRITE


# END_FUNCTION_save_config
