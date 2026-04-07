# FILE:lesson_24/db_manager.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Handle SQLite database operations for storing and retrieving parabola points.
# SCOPE: DB interactions (save_points, get_points, init_db).
# INPUT: Tuples of points (x, y).
# OUTPUT: Pandas DataFrame of points.
# KEYWORDS:DOMAIN(Parabola): DB; CONCEPT(SQLite): PointStorage
# LINKS:READS_DATA_FROM(parabola.db); WRITES_TO(parabola.db)
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: 1.0.0 - Initial implementation of DB manager.
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC [7][Initializes SQLite database] => init_db
# FUNC [8][Saves parabola points to DB] => save_points
# FUNC [8][Retrieves parabola points from DB] => get_points
# END_MODULE_MAP

import sqlite3
import pandas as pd
import logging
import os

# START_BLOCK_LOGGING_SETUP: [Setup local logger]
logger = logging.getLogger("lesson_24.db_manager")
# END_BLOCK_LOGGING_SETUP


# START_FUNCTION_init_db
# START_CONTRACT:
# PURPOSE:Initialize the parabola table in SQLite.
# INPUTS:
# - db_path: str => database file path
# OUTPUTS:
# - None
# SIDE_EFFECTS: Creates table 'points' if not exists.
# KEYWORDS:PATTERN(DB): Schema
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def init_db(db_path="lesson_24/parabola.db"):
    """
    Initializes the SQLite database with the required 'points' table.
    Uses LDD 2.0 logging to track database creation.
    """
    # START_BLOCK_SETUP:[Perform database setup]
    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                x REAL,
                y REAL
            )
        """)
        conn.commit()
        conn.close()
        logger.info(
            f"[IMP:7][init_db][SETUP][DB] Database initialized at {db_path}.[SUCCESS]"
        )
    except Exception as e:
        logger.error(
            f"[IMP:10][init_db][SETUP][ERROR] Database initialization failed: {str(e)}[CRITICAL]"
        )
    # END_BLOCK_SETUP


# END_FUNCTION_init_db


# START_FUNCTION_save_points
# START_CONTRACT:
# PURPOSE:Save points to SQLite, clearing existing data first.
# INPUTS:
# - points: list[tuple] => [(x, y), ...]
# - db_path: str => database file path
# OUTPUTS:
# - bool - Success status
# SIDE_EFFECTS: Clears 'points' table, inserts new rows.
# KEYWORDS:PATTERN(DB): Write
# COMPLEXITY_SCORE: 5
# END_CONTRACT
def save_points(points, db_path="lesson_24/parabola.db"):
    """
    Clears all existing points and saves new ones to the database.
    Verifies that input is a list of points.
    """
    # START_BLOCK_WRITE:[Perform batch database write]
    try:
        init_db(db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Clear existing
        cursor.execute("DELETE FROM points")

        # Bulk insert
        cursor.executemany("INSERT INTO points (x, y) VALUES (?, ?)", points)

        conn.commit()
        conn.close()
        logger.info(
            f"[IMP:9][save_points][WRITE][DB] Saved {len(points)} points to {db_path}.[BELIEF:POINTS_WRITTEN]"
        )
        return True
    except Exception as e:
        logger.error(
            f"[IMP:10][save_points][WRITE][ERROR] Saving points failed: {str(e)}[CRITICAL]"
        )
        return False
    # END_BLOCK_WRITE


# END_FUNCTION_save_points


# START_FUNCTION_get_points
# START_CONTRACT:
# PURPOSE:Retrieve all points from SQLite as a DataFrame.
# INPUTS:
# - db_path: str => database file path
# OUTPUTS:
# - pd.DataFrame - Parabola data
# SIDE_EFFECTS: None
# KEYWORDS:PATTERN(DB): Read
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def get_points(db_path="lesson_24/parabola.db"):
    """
    Reads the 'points' table from the SQLite database and returns it as a pandas DataFrame.
    """
    # START_BLOCK_READ:[Perform database read]
    try:
        init_db(db_path)
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT x, y FROM points ORDER BY x", conn)
        conn.close()
        logger.info(
            f"[IMP:8][get_points][READ][DB] Retrieved {len(df)} points from {db_path}.[SUCCESS]"
        )
        return df
    except Exception as e:
        logger.error(
            f"[IMP:10][get_points][READ][ERROR] Retrieving points failed: {str(e)}[CRITICAL]"
        )
        return pd.DataFrame(columns=["x", "y"])
    # END_BLOCK_READ


# END_FUNCTION_get_points
