""" Модуль unit-тестов для models.py. """

import unittest from models import Client, Product, Order, SpecialOrder, print_order_cost

class TestModels(unittest.TestCase): def test_client_validation(self): client = Client("Иван", "+1234567890", "ivan@example.com") self.assertTrue(client.validate()) invalid_client = Client("Петр", "12345", "not-an-email") self.assertFalse(invalid_client.validate())

def test_order_total_cost(self):
    product1 = Product("Товар 1", "Описание", 100)
    product2 = Product("Товар 2", "Описание", 200)
    client = Client("Анна", "+1234567891", "anna@example.com")
    order = Order(client, [(product1, 2), (product2, 1)], "2023-10-10 10:00:00")
    self.assertEqual(order.total_cost(), 2*100 + 200)

def test_special_order_total_cost(self):
    product = Product("Товар", "Описание", 100)
    client = Client("Сергей", "+1234567892", "sergey@example.com")
    order = SpecialOrder(client, [(product, 3)], "2023-10-10 12:00:00", discount=10)
    self.assertAlmostEqual(order.total_cost(), 3*100*0.9)
if name == "main": unittest.main()