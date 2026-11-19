"""Tiny module used as a citation fixture by the script tests."""
import math


def circle_area(radius):
    if radius < 0:
        raise ValueError("radius must be non-negative")
    return math.pi * radius ** 2


def square_area(side):
    """Area of a square."""
    return side * side


def perimeter(sides):
    return sum(sides)
