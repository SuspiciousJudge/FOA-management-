def calculate_order_total(items, discount=0):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    total = total - (total * discount / 100)
    return round(total, 2)


def add_to_cart(cart, item):
    for i in cart:
        if i['name'] == item['name']:
            i['quantity'] += item['quantity']
            return cart
    cart.append(item.copy())
    return cart


def remove_from_cart(cart, name):
    return [i for i in cart if i['name'] != name]
