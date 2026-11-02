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
        [{'name': 'Soda', 'price': 3.0, 'quantity': 0}],
        0,
        0.0
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
    (
        [{'name': 'Wrap', 'price': 10.0, 'quantity': 1}],
        99,
        0.1
    ),
])
def test_calculate_order_total(items, discount, expected):
    result = calculate_order_total(items, discount)
    assert result == expected


def test_invalid_discount_over_100():
    items = [{'name': 'Burger', 'price': 5.0, 'quantity': 1}]
    result = calculate_order_total(items, discount=150)
    assert result < 0


def test_negative_price():
    items = [{'name': 'Burger', 'price': -5.0, 'quantity': 2}]
    result = calculate_order_total(items)
    assert result == -10.0


def test_negative_discount():
    items = [{'name': 'Pizza', 'price': 10.0, 'quantity': 1}]
    result = calculate_order_total(items, discount=-10)
    assert result == 11.0
