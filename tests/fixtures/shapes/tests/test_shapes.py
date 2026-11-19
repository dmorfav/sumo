from shapes import circle_area, perimeter, square_area


def test_circle_area_of_unit_radius():
    assert round(circle_area(1), 5) == 3.14159


def test_perimeter_of_triangle():
    assert perimeter([3, 4, 5]) == 12


def test_square_area():
    side = 3
    expected = 9
    assert square_area(side) == expected
