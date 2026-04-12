# FILE:lesson_25/generator.py
# VERSION:1.0.0
# START_MODULE_CONTRACT:
# PURPOSE:Core calculation logic for parabola points y = ax^2 + c.
# SCOPE:Mathematical generation of points within a given range.
# INPUT:Coefficients a, c and range x_min, x_max.
# OUTPUT:DataFrame with columns x and y.
# KEYWORDS:[DOMAIN(8):Mathematics; CONCEPT(7):Calculation; TECH(9):Numpy]
# LINKS:[USES_API(8):numpy]
# END_MODULE_CONTRACT

# START_RATIONALE:
# Q: Why use numpy for point generation?
# A: Efficient vectorized calculation of y = ax^2 + c, and easy range generation using linspace.
# END_RATIONALE

# START_CHANGE_SUMMARY:
# LAST_CHANGE: [v1.0.0 - Initial implementation of generator logic.]
# END_CHANGE_SUMMARY

# START_MODULE_MAP:
# FUNC 10[Generates parabola points] => generate_parabola_points
# END_MODULE_MAP

import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)


# START_FUNCTION_generate_parabola_points
# START_CONTRACT:
# PURPOSE:Calculates y = ax^2 + c for a range of x values.
# INPUTS:
# - float => a: x^2 coefficient.
# - float => c: constant coefficient.
# - float => x_min: start of range.
# - float => x_max: end of range.
# - int => num_points: granularity of the calculation (default 100).
# OUTPUTS:
# - DataFrame - calculated points (x, y).
# SIDE_EFFECTS: None
# KEYWORDS:[PATTERN(8):Vectorization; CONCEPT(7):Parabola]
# COMPLEXITY_SCORE: 3
# END_CONTRACT
def generate_parabola_points(
    a: float, c: float, x_min: float, x_max: float, num_points: int = 100
) -> pd.DataFrame:
    """
    Function generates a set of points for a parabola defined by coefficients a and c.
    It uses numpy to create a linear space for x and then applies the formula y = ax^2 + c.
    Returns a pandas DataFrame for compatibility with UI and DB modules.
    """

    # START_BLOCK_VALIDATION: [Checking input validity]
    if x_min >= x_max:
        logger.warning(
            f"[LogicCheck][IMP:6][generate_parabola_points][VALIDATION][Condition] x_min ({x_min}) >= x_max ({x_max}). Reverting to default range [-10, 10]."
        )
        x_min, x_max = -10.0, 10.0
    # END_BLOCK_VALIDATION

    # START_BLOCK_CALCULATION: [Numpy vectorized generation]
    logger.debug(
        f"[Math][IMP:4][generate_parabola_points][CALCULATION][Params] a={a}, c={c}, range=[{x_min}, {x_max}]"
    )

    x_values = np.linspace(x_min, x_max, num_points)
    y_values = a * (x_values**2) + c

    df = pd.DataFrame({"x": x_values, "y": y_values})
    # END_BLOCK_CALCULATION

    # START_BLOCK_RETURN: [Finalizing result]
    logger.info(
        f"[BeliefState][IMP:9][generate_parabola_points][RETURN][Flow] Generated {len(df)} points for parabola. [VALUE]"
    )
    return df
    # END_BLOCK_RETURN


# END_FUNCTION_generate_parabola_points
