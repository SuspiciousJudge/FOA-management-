def calculate_order_total(items, discount=0):
    """Calculate total price after applying a percentage discount."""
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    discount_amount = subtotal * (discount / 100)
    return round(subtotal - discount_amount, 2)


def add_to_cart(cart, item):
    """Add an item to the cart or increase quantity if it exists."""
    for existing in cart:
        if existing['name'] == item['name']:
            existing['quantity'] += item['quantity']
            return cart
    cart.append(item.copy())
    return cart


def remove_from_cart(cart, item_name):
    """Remove an item from the cart by name."""
    return [item for item in cart if item['name'] != item_name]


def get_cart_total(cart):
    """Return total price for all items in the cart."""
    return calculate_order_total(cart)
