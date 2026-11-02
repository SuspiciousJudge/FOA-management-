class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity=1):
        for item in self.items:
            if item['name'] == name:
                item['quantity'] += quantity
                return
        self.items.append({'name': name, 'price': price, 'quantity': quantity})

    def remove_item(self, name):
        self.items = [i for i in self.items if i['name'] != name]

    def total(self):
        t = 0
        for item in self.items:
            t += item['price'] * item['quantity']
        return round(t, 2)

    def clear(self):
        self.items = []
