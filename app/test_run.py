import pytest
from app import calculate_order_total, add_to_cart, remove_from_cart, get_cart_total


# --- calculate_order_total tests ---

def test_order_total_no_discount():
    items = [{'name': 'Burger', 'price': 5.0, 'quantity': 2}]
    assert calculate_order_total(items) == 10.0


def test_order_total_with_discount():
    items = [{'name': 'Pizza', 'price': 10.0, 'quantity': 1}]
    assert calculate_order_total(items, discount=10) == 9.0


def test_order_total_multiple_items():
    items = [
        {'name': 'Burger', 'price': 5.0, 'quantity': 2},
        {'name': 'Fries', 'price': 2.0, 'quantity': 3},
    ]
    assert calculate_order_total(items) == 16.0


def test_order_total_zero_items():
    assert calculate_order_total([]) == 0.0


def test_order_total_100_percent_discount():
    items = [{'name': 'Salad', 'price': 8.0, 'quantity': 1}]
    assert calculate_order_total(items, discount=100) == 0.0


# --- add_to_cart tests ---

def test_add_new_item_to_cart():
    cart = []
    item = {'name': 'Burger', 'price': 5.0, 'quantity': 1}
    cart = add_to_cart(cart, item)
    assert len(cart) == 1
    assert cart[0]['name'] == 'Burger'


def test_add_existing_item_increases_quantity():
    cart = [{'name': 'Burger', 'price': 5.0, 'quantity': 1}]
    cart = add_to_cart(cart, {'name': 'Burger', 'price': 5.0, 'quantity': 2})
    assert cart[0]['quantity'] == 3


# --- remove_from_cart tests ---

def test_remove_item_from_cart():
    cart = [
        {'name': 'Burger', 'price': 5.0, 'quantity': 1},
        {'name': 'Fries', 'price': 2.0, 'quantity': 1},
    ]
    cart = remove_from_cart(cart, 'Burger')
    assert len(cart) == 1
    assert cart[0]['name'] == 'Fries'


def test_remove_nonexistent_item_leaves_cart_unchanged():
    cart = [{'name': 'Pizza', 'price': 10.0, 'quantity': 1}]
    cart = remove_from_cart(cart, 'Sushi')
    assert len(cart) == 1
