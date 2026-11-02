import pytest
from app import calculate_order_total


@pytest.mark.parametrize("items, discount, expected", [
    (
        [{'name': 'Burger', 'price': 5.0, 'quantity': 2},
         {'name': 'Fries',  'price': 2.0, 'quantity': 3}],
        10,
        14.4
    ),
    (
        [{'name': 'Pizza', 'price': 10.0, 'quantity': 1}],
        0,
        10.0
    ),
    (
        [],
        0,
        0.0
    ),
    (
        [{'name': 'Sandwich', 'price': 8.0, 'quantity': 1}],
        100,
        0.0
    ),
])
def test_calculate_order_total(items, discount, expected):
    result = calculate_order_total(items, discount)
    assert result == expected
