import unittest
from django.test import Client
from main.views import HomeView, CheckoutView, OrderSummaryView, ItemDetailView, add_to_cart, remove_from_cart, remove_single_item_from_cart


class TestUrls(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_home(self):
        # Issue a GET request.
        response = self.client.get('')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_checkout(self):
        response = self.client.get('checkout/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    # def test_order_summary(self):
    #     response = self.client.get('order-summary/')

    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)

    # def test_product(self):
    #     response = self.client.get('product/23563/')

    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)

    # def test_add_to_cart(self):
    #     response = self.client.get('add-to-cart/23563/')

    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)

    # def test_remove_from_cart(self):
    #     response = self.client.get(
    #         'remove-from-cart/23563/')

    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)

    # def test_remove_item_from_cart(self):
    #     response = self.client.get(
    #         'remove-item-from-cart/23563/')

    #     # Check that the response is 200 OK.
    #     self.assertEqual(response.status_code, 200)
