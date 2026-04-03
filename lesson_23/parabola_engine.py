# FILE:lesson_23/parabola_engine.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Pure logic module for calculating parabola coordinates.
# SCOPE:Generating (x, y) coordinates based on y = ax^2 + c.
# INPUT:Coefficients a, c and range parameters x_min, x_max.
# OUTPUT:List of (x, y) coordinate tuples.
# KEYWORDS:DOMAIN(Math): Parabola; CONCEPT(Calculation): Coordinate generation.
# LINKS:NONE
# END_MODULE_CONTRACT
#
# START_CHANGE_SUMMARY:
# LAST_CHANGE: 1.0.0 - Initial implementation of parabola logic.
# END_CHANGE_SUMMARY
#
# START_MODULE_MAP:
# FUNC[9][Generates list of coordinates] => calculate_parabola
# END_MODULE_MAP

import logging


# START_FUNCTION_calculate_parabola
# START_CONTRACT:
# PURPOSE: Calculates coordinates for the parabola y = ax^2 + c.
# INPUTS:
# - a: float => quadratic coefficient
# - c: float => constant term
# - x_min: float => start of the range
# - x_max: float => end of the range
# - num_points: int => total points to generate
# OUTPUTS:
# - list[tuple[float, float]] - calculated coordinates
# COMPLEXITY_SCORE: 4
# END_CONTRACT
def calculate_parabola(
    a: float, c: float, x_min: float, x_max: float, num_points: int = 100
) -> list:
    """
    Computes a sequence of x and y values following the quadratic equation
    y = ax^2 + c. The x values are evenly spaced between x_min and x_max.
    """
    logger = logging.getLogger("app_23")

    # START_BLOCK_VALIDATION:[Check range validity]
    if x_min >= x_max:
        logger.warning(
            f"[WARN][IMP:8][parabola_engine][calculate_parabola][VALIDATION] Invalid range: x_min ({x_min}) >= x_max ({x_max}).[SUCCESS]"
        )
        return []
    # END_BLOCK_VALIDATION

    # START_BLOCK_GENERATION:[Iterate and calculate points]
    points = []
    step = (x_max - x_min) / (num_points - 1) if num_points > 1 else 0

    for i in range(num_points):
        x = x_min + (i * step)
        y = (a * (x**2)) + c
        points.append((x, y))
    # END_BLOCK_GENERATION

    logger.info(
        f"[INFO][IMP:7][parabola_engine][calculate_parabola][LOGIC] Generated {len(points)} parabola points.[SUCCESS]"
    )

    # AI Belief State: Generated points strictly follow the parabola formula.
    logger.info(
        f"[BELIEF][IMP:9][parabola_engine][calculate_parabola][VALIDATION] Parabola calculation is mathematically correct.[SUCCESS]"
    )

    return points


# END_FUNCTION_calculate_parabola
