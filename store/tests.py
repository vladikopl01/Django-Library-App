from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import all_products


class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_model_string(self):
        """
        Test Category model default name
        """
        data = self.data1
        self.assertEqual(str(data), 'django')


class TestProductModel(TestCase):
    def setUp(self):
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(
            category_id=1, title='django beginners', created_by_id=1,
            slug='django-beginners', price='120.00', image='django'
        )

    def test_products_model_entry(self):
        """
        Test Product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))

    def test_products_model_string(self):
        """
        Test Product model default name
        """
        data = self.data1
        self.assertEqual(str(data), 'django beginners')


class TestViewResponse(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                               slug='django-beginners', price='120.00', image='django')

    def test_url_allowed_hosts(self):
        """
        Test homepage response status
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        Test detail product response status
        """
        response = self.c.get(reverse('store:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)

    def test_category_detail_url(self):
        """
        Test detail product response status
        """
        response = self.c.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Test homepage response status by HttpRequest
        """
        request = HttpRequest()
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home page</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        """
        Test homepage response status by RequestFactory
        """
        request = self.factory.get('/item/django-beginners')
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home page</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
