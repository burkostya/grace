# FILE:lesson_24/logic.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Calculate the coordinates of parabola points based on parameters a, c, and range x_min to x_max.
# SCOPE: Mathematical calculation of y = ax^2 + c.
# INPUT: Coefficients a, c; Range x_min, x_max.
# OUTPUT: List of (x, y) tuples.
# KEYWORDS:DOMAIN(Parabola): Math; CONCEPT(Calculation): ParabolaPoints
# LINKS:None
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: 1.0.0 - Initial implementation of parabola logic.
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC [9][Calculates (x, y) coordinates for parabola] => calculate_parabola
# END_MODULE_MAP

import numpy as np
import logging

# START_BLOCK_LOGGING_SETUP: [Setup local logger]
logger = logging.getLogger("lesson_24.logic")
# END_BLOCK_LOGGING_SETUP


# START_FUNCTION_calculate_parabola
# START_CONTRACT:
# PURPOSE:Calculate the coordinates of parabola points for a given range and parameters.
# INPUTS:
# - a: float => Coefficient a
# - c: float => Coefficient c
# - x_min: float => Range start
# - x_max: float => Range end
# - num_points: int => Number of points to generate
# OUTPUTS:
# - list[tuple] - Calculated (x, y) points
# SIDE_EFFECTS: None
# KEYWORDS:PATTERN(Logic): Math
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def calculate_parabola(a, c, x_min, x_max, num_points=100):
    """
    Computes a set of points for the parabola y = ax^2 + c.
    Generates 'num_points' evenly spaced x-values between x_min and x_max.
    Logs the calculation parameters as part of LDD belief state.
    """
    # START_BLOCK_CALC:[Perform mathematical calculation]
    try:
        # AI Belief: Calculate parabola using y = ax^2 + c
        logger.info(
            f"[IMP:9][calculate_parabola][CALC][LOGIC] Calculating y = {a}*x^2 + {c} in [{x_min}, {x_max}].[BELIEF:PARABOLA_MATH]"
        )

        # Linear space for x
        x_values = np.linspace(x_min, x_max, num_points)

        # Vectorized calculation for y
        y_values = a * (x_values**2) + c

        # Combine into list of tuples
        points = list(zip(x_values, y_values))

        logger.info(
            f"[IMP:8][calculate_parabola][CALC][LOGIC] Generated {len(points)} points for parabola.[SUCCESS]"
        )
        return points
    except Exception as e:
        logger.error(
            f"[IMP:10][calculate_parabola][CALC][ERROR] Calculation failed: {str(e)}[CRITICAL]"
        )
        return []
    # END_BLOCK_CALC


# END_FUNCTION_calculate_parabola
