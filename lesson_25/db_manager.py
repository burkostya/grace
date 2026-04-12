# FILE:lesson_25/db_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Manages SQLite storage for parabola points in Lesson 25.
# SCOPE:Table initialization, bulk insertion of points, and retrieval.
# INPUT:List of (x, y) tuples or DataFrame.
# OUTPUT:DataFrame of points.
# KEYWORDS:[DOMAIN(8):Database; CONCEPT(7):SQL; TECH(9):SQLite]
# LINKS:[USES_API(8):sqlite3; READS_DATA_FROM(9):lesson_25/parabola_25.db]
# END_MODULE_CONTRACT

# START_RATIONALE:
# Q: Why use pandas for DB operations?
# A: Simplifies to_sql and read_sql_query operations, making the code more readable for agents.
# END_RATIONALE

# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Initial implementation of DBManager.]
# END_CHANGE_SUMMARY

# START_MODULE_MAP:
# CLASS 10[Handles SQLite operations for parabola points] => DBManager
# END_MODULE_MAP

import sqlite3
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)


# START_FUNCTION_DBManager
class DBManager:
    """
    DBManager encapsulates all interactions with the SQLite database.
    It ensures the points table exists and provides methods to persist and retrieve data.
    """

    def __init__(self, db_path="lesson_25/parabola_25.db"):
        self.db_path = db_path
        self._init_db()
        logger.debug(
            f"[DB][IMP:4][DBManager][init][Flow] Initialized with path: {self.db_path}"
        )

    # START_FUNCTION__init_db
    def _init_db(self):
        """
        Creates the 'points' table if it does not exist.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS points (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        x REAL,
                        y REAL
                    )
                """)
            logger.info(
                f"[DB][IMP:7][DBManager][init_db][IO] Database initialized at {self.db_path}"
            )
        except sqlite3.Error as e:
            logger.critical(
                f"[SystemError][IMP:10][DBManager][init_db][Exception] Failed to init DB: {e}"
            )

    # END_FUNCTION__init_db

    # START_FUNCTION_save_points
    # START_CONTRACT:
    # PURPOSE:Saves a list of points to the database, clearing old data.
    # INPUTS: - list/DataFrame => points: data to save.
    # OUTPUTS: - bool - success status.
    # SIDE_EFFECTS: Clears 'points' table and inserts new data.
    # COMPLEXITY_SCORE: 5
    # END_CONTRACT
    def save_points(self, points) -> bool:
        """
        Takes a list of points or a DataFrame and persists it to the SQLite table.
        Old points are replaced to ensure only current calculation is stored.
        """
        # START_BLOCK_PREPARE_DF: [Ensuring data is in DataFrame format]
        if isinstance(points, list):
            df = pd.DataFrame(points, columns=["x", "y"])
        else:
            df = points
        # END_BLOCK_PREPARE_DF

        # START_BLOCK_SQL_PERSIST: [Saving to database]
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Clear old points
                conn.execute("DELETE FROM points")
                # Write new points
                df.to_sql("points", conn, if_exists="append", index=False)
            logger.info(
                f"[BeliefState][IMP:9][DBManager][save_points][IO] Successfully saved {len(df)} points to DB. [SUCCESS]"
            )
            return True
        except (sqlite3.Error, pd.errors.DatabaseError) as e:
            logger.critical(
                f"[SystemError][IMP:10][DBManager][save_points][Exception] Failed to save points: {e}"
            )
            return False
        # END_BLOCK_SQL_PERSIST

    # END_FUNCTION_save_points

    # START_FUNCTION_get_points
    # START_CONTRACT:
    # PURPOSE:Retrieves all points from the database.
    # INPUTS: None
    # OUTPUTS: - DataFrame - points from DB.
    # SIDE_EFFECTS: None
    # COMPLEXITY_SCORE: 4
    # END_CONTRACT
    def get_points(self) -> pd.DataFrame:
        """
        Reads all rows from the 'points' table into a pandas DataFrame.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query("SELECT x, y FROM points ORDER BY x", conn)
            logger.debug(
                f"[DB][IMP:7][DBManager][get_points][IO] Retrieved {len(df)} points from DB."
            )
            return df
        except (sqlite3.Error, pd.errors.DatabaseError) as e:
            logger.critical(
                f"[SystemError][IMP:10][DBManager][get_points][Exception] Failed to read points: {e}"
            )
            return pd.DataFrame(columns=["x", "y"])

    # END_FUNCTION_get_points


# END_FUNCTION_DBManager
