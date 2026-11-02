import pytest
from app import calculate_order_total


# ── parametrized tests ────────────────────────────────────────────────────────

@pytest.mark.parametrize("items, discount, expected", [
    # normal case
    (
        [{'name': 'Burger', 'price': 5.0, 'quantity': 2},
         {'name': 'Fries',  'price': 2.0, 'quantity': 3}],
        10,
        14.4
    ),
    # zero discount
    (
        [{'name': 'Pizza', 'price': 10.0, 'quantity': 1}],
        0,
        10.0
    ),
    # zero quantity (empty-like item)
    (
        [{'name': 'Soda', 'price': 3.0, 'quantity': 0}],
        0,
        0.0
    ),
    # empty cart
    (
        [],
        0,
        0.0
    ),
    # boundary: 100% discount
    (
        [{'name': 'Sandwich', 'price': 8.0, 'quantity': 1}],
        100,
        0.0
    ),
    # boundary: discount just under 100
    (
        [{'name': 'Wrap', 'price': 10.0, 'quantity': 1}],
        99,
        0.1
    ),
])
def test_calculate_order_total(items, discount, expected):
    result = calculate_order_total(items, discount)
    assert result == expected, f"Expected {expected} but got {result}"


# ── invalid input tests ───────────────────────────────────────────────────────

def test_invalid_discount_over_100():
    items = [{'name': 'Burger', 'price': 5.0, 'quantity': 1}]
    # discount > 100 gives negative total — function does not guard against it
    result = calculate_order_total(items, discount=150)
    assert result < 0  # expected behaviour without validation


def test_negative_price():
    items = [{'name': 'Burger', 'price': -5.0, 'quantity': 2}]
    result = calculate_order_total(items)
    assert result == -10.0  # no validation — negative propagates


def test_negative_discount():
    items = [{'name': 'Pizza', 'price': 10.0, 'quantity': 1}]
    result = calculate_order_total(items, discount=-10)
    assert result == 11.0  # negative discount increases total
