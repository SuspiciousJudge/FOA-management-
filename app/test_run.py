import pytest
from app import calculate_order_total, add_to_cart, remove_from_cart


def test_total_no_discount():
    items = [{'name': 'Burger', 'price': 5.0, 'quantity': 2}]
    assert calculate_order_total(items) == 10.0


def test_total_with_discount():
    items = [{'name': 'Pizza', 'price': 10.0, 'quantity': 1}]
    assert calculate_order_total(items, discount=10) == 9.0


def test_total_multiple_items():
    items = [
        {'name': 'Burger', 'price': 5.0, 'quantity': 2},
        {'name': 'Fries', 'price': 2.0, 'quantity': 3},
    ]
    assert calculate_order_total(items) == 16.0


def test_empty_cart():
    assert calculate_order_total([]) == 0.0


def test_add_new_item():
    cart = []
    cart = add_to_cart(cart, {'name': 'Burger', 'price': 5.0, 'quantity': 1})
    assert len(cart) == 1


def test_add_same_item_twice():
    cart = [{'name': 'Burger', 'price': 5.0, 'quantity': 1}]
    cart = add_to_cart(cart, {'name': 'Burger', 'price': 5.0, 'quantity': 1})
    assert cart[0]['quantity'] == 2


def test_remove_item():
    cart = [
        {'name': 'Burger', 'price': 5.0, 'quantity': 1},
        {'name': 'Fries', 'price': 2.0, 'quantity': 1},
    ]
    cart = remove_from_cart(cart, 'Burger')
    assert len(cart) == 1
    assert cart[0]['name'] == 'Fries'


def test_remove_item_not_in_cart():
    cart = [{'name': 'Pizza', 'price': 10.0, 'quantity': 1}]
    cart = remove_from_cart(cart, 'Sushi')
    assert len(cart) == 1
