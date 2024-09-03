#!/usr/bin/env python3
""" multiplying floats"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """returns a function that multiplies a float by multiplier"""
    def function(n: float):
        return n * multiplier

    return function
