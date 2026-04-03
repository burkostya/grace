# FILE:lesson_23/db_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Manages the SQLite database for parabola points.
# SCOPE:Creating table, saving calculated points, and retrieving for display/plotting.
# INPUT:List of (x, y) tuples or database file path.
# OUTPUT:Pandas DataFrame or success status.
# KEYWORDS:DOMAIN(DB): SQL data persistence; CONCEPT(Points): Parabola trajectory.
# LINKS:USES_API(sqlite3); USES_API(pandas)
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: 1.0.0 - Initial implementation of DBManager.
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# CLASS[8][Handles SQL data management] => DBManager
# FUNC[7][Initializes database schema] => DBManager.init_db
# FUNC[8][Saves parabola points to database] => DBManager.save_points
# FUNC[7][Retrieves points as pandas DataFrame] => DBManager.get_points
# END_MODULE_MAP

import sqlite3
import pandas as pd
import logging
import os


# START_FUNCTION_DBManager
class DBManager:
    """
    Manager for parabola data in SQLite. Provides structured storage and
    easy retrieval into pandas for Gradio/Plotly.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.logger = logging.getLogger("app_23")

    # START_FUNCTION_init_db
    # START_CONTRACT:
    # PURPOSE: Ensures the parabola_points table exists.
    # INPUTS: None
    # OUTPUTS: bool - Success status.
    # COMPLEXITY_SCORE: 3
    # END_CONTRACT
    def init_db(self) -> bool:
        """
        Creates the parabola_points table if it doesn't already exist.
        """
        # START_BLOCK_SQL_EXEC:[Create table]
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS parabola_points (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        x REAL NOT NULL,
                        y REAL NOT NULL
                    )
                """)
            self.logger.info(
                f"[INFO][IMP:7][DBManager][init_db][SQL] Database initialized successfully.[SUCCESS]"
            )
            return True
        except Exception as e:
            self.logger.error(
                f"[ERROR][IMP:10][DBManager][init_db][CRITICAL] Failed to init DB: {e}[FAILURE]"
            )
            return False
        # END_BLOCK_SQL_EXEC

    # END_FUNCTION_init_db

    # START_FUNCTION_save_points
    # START_CONTRACT:
    # PURPOSE: Clears old points and saves new ones.
    # INPUTS: - points: list[tuple[float, float]] => list of (x, y) coordinates
    # OUTPUTS: bool - Success status.
    # COMPLEXITY_SCORE: 5
    # END_CONTRACT
    def save_points(self, points: list) -> bool:
        """
        Clears existing data and inserts a new set of points into the database.
        """
        # START_BLOCK_TRANSACTION:[Transactional delete and insert]
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM parabola_points")
                conn.executemany(
                    "INSERT INTO parabola_points (x, y) VALUES (?, ?)", points
                )
            self.logger.info(
                f"[INFO][IMP:8][DBManager][save_points][SQL] Saved {len(points)} points.[SUCCESS]"
            )
            return True
        except Exception as e:
            self.logger.error(
                f"[ERROR][IMP:10][DBManager][save_points][CRITICAL] Failed to save points: {e}[FAILURE]"
            )
            return False
        # END_BLOCK_TRANSACTION

    # END_FUNCTION_save_points

    # START_FUNCTION_get_points
    # START_CONTRACT:
    # PURPOSE: Retrieves all points as a DataFrame.
    # INPUTS: None
    # OUTPUTS: pd.DataFrame - Parabola data.
    # COMPLEXITY_SCORE: 4
    # END_CONTRACT
    def get_points(self) -> pd.DataFrame:
        """
        Reads points from SQLite and converts them into a pandas DataFrame.
        """
        # START_BLOCK_READ_SQL:[Select and convert to DataFrame]
        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query(
                    "SELECT x, y FROM parabola_points ORDER BY x ASC", conn
                )
            self.logger.info(
                f"[INFO][IMP:7][DBManager][get_points][SQL] Loaded {len(df)} points into DataFrame.[SUCCESS]"
            )
            return df
        except Exception as e:
            self.logger.error(
                f"[ERROR][IMP:10][DBManager][get_points][CRITICAL] Failed to get points: {e}[FAILURE]"
            )
            return pd.DataFrame(columns=["x", "y"])
        # END_BLOCK_READ_SQL

    # END_FUNCTION_get_points


# END_FUNCTION_DBManager
