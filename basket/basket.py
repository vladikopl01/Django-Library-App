from decimal import Decimal

from store.models import Product


class Basket():
    """
    A Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def __len__(self):
        """
        Get the basket data and quantity of items
        """
        return sum(item['qty'] for item in self.basket.values())

    def __iter__(self):
        """
        Collect the product product_id in the session data 
        to query the database and return products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def add(self, product, quantity):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = quantity
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': int(quantity)}
            self.save()

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def update(self, product, qty):
        """
        Update quantity item in session data
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum([Decimal(item['price']) * item['qty'] for item in self.basket.values()])
