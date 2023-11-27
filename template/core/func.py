# template/core/func.py

"""Provide core functions

This module allows the user to make calculations.

Examples:
    >>> from template.core import addInt
    >>> addInt(2, 4)
    6
  
The module contains the following functions:

- `addInt(a, b)` - Returns the sum of two integer.
"""

def addInt(x: int, y: int) -> int:
    return x + y
