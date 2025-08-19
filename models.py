import re

class Entity: """ Базовый класс для всех сущностей проекта.

Parameters
----------
id : int, optional
    Идентификатор сущности, по умолчанию None.
"""
def __init__(self, id=None):
    self._id = id  # Инкапсуляция: защищённое поле для идентификатора

@property
def id(self):
    """Получить идентификатор."""
    return self._id

@id.setter
def id(self, value):
    self._id = value

def __str__(self):
    return f"{self.__class__.__name__}(id={self._id})"
class Client(Entity): """ Класс клиента. Содержит данные о клиенте и методы валидации контактов (телефон, email).

Parameters
----------
name : str
    Имя клиента.
phone : str
    Телефон клиента.
email : str
    Email клиента.
id : int, optional
    Идентификатор клиента, по умолчанию None.
"""
def __init__(self, name, phone, email, id=None):
    super().__init__(id)
    self.name = name
    self.phone = phone
    self.email = email

def validate(self):
    """
    Валидирует телефон и email клиента с использованием регулярных выражений.

    Returns
    -------
    bool
        True, если телефон и email соответствуют требованиям, иначе False.
    """
    phone_pattern = r"^\+?\d{7,15}$"
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    valid_phone = re.match(phone_pattern, self.phone)
    valid_email = re.match(email_pattern, self.email)
    return bool(valid_phone and valid_email)

def __str__(self):
    return f"Client(id={self.id}, name={self.name})"
class Product(Entity): """ Класс товара.

Parameters
----------
name : str
    Наименование товара.
description : str
    Описание товара.
price : float
    Цена товара.
id : int, optional
    Идентификатор товара, по умолчанию None.
"""
def __init__(self, name, description, price, id=None):
    super().__init__(id)
    self.name = name
    self.description = description
    self.price = price

def __str__(self):
    return f"Product(id={self.id}, name={self.name}, price={self.price})"
class Order(Entity): """ Класс заказа.

Parameters
----------
client : Client
    Клиент, сделавший заказ.
products : list of tuple(Product, int)
    Список кортежей, где каждый кортеж содержит объект Product и количество (int).
order_date : str
    Дата заказа.
id : int, optional
    Идентификатор заказа, по умолчанию None.
"""
def __init__(self, client, products, order_date, id=None):
    super().__init__(id)
    self.client = client
    self.products = products  # [(Product, количество)]
    self.order_date = order_date

def total_cost(self):
    """
    Рассчитывает общую стоимость заказа.

    Returns
    -------
    float
        Суммарная стоимость заказа.
    """
    return sum(product.price * qty for product, qty in self.products)

def __str__(self):
    return f"Order(id={self.id}, client={self.client.name}, date={self.order_date}, total_cost={self.total_cost()})"
class SpecialOrder(Order): """ Наследник Order для специальных заказов со скидкой.

Parameters
----------
discount : float
    Скидка в процентах, применяемая к сумме заказа.
"""
def __init__(self, client, products, order_date, discount, id=None):
    super().__init__(client, products, order_date, id)
    self.discount = discount

def total_cost(self):
    """
    Рассчитывает общую стоимость заказа с учётом скидки.

    Returns
    -------
    float
        Итоговая сумма заказа со скидкой.
    """
    total = super().total_cost()
    return total * (1 - self.discount / 100)

def __str__(self):
    return f"SpecialOrder(id={self.id}, client={self.client.name}, date={self.order_date}, total_cost={self.total_cost()}, discount={self.discount}%)"
def print_order_cost(order): """ Демонстрация полиморфизма: вывод стоимости заказа, независимо от того, обычный ли это заказ или специальный.

Parameters
----------
order : Order
    Объект заказа.
"""
print(f"Заказ клиента {order.client.name} стоит {order.total_cost():.2f}")