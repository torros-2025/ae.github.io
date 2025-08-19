""" Модуль db.py Содержит класс Database для работы с SQLite, а также для импорта/экспорта данных в CSV и JSON. """

import sqlite3 import csv import json from datetime import datetime from models import Client, Product, Order, SpecialOrder

class Database: """ Класс для работы с базой SQLite и файловыми форматами.

Parameters
----------
db_name : str
    Имя файла базы данных.
"""
def __init__(self, db_name="shop.db"):
    self.conn = sqlite3.connect(db_name)
    self.create_tables()

def create_tables(self):
    """Создаёт таблицы clients, products, orders, order_details, если они отсутствуют."""
    cursor = self.conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_date TEXT NOT NULL,
                client_id INTEGER,
                discount REAL DEFAULT 0,
                FOREIGN KEY(client_id) REFERENCES clients(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                price REAL,
                FOREIGN KEY(order_id) REFERENCES orders(id),
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        """)
        self.conn.commit()
    except sqlite3.Error as e:
        print("Ошибка при создании таблиц:", e)

def add_client(self, client):
    """
    Добавляет объект Client в базу данных.

    Parameters
    ----------
    client : Client
        Объект клиента.
    """
    cursor = self.conn.cursor()
    try:
        cursor.execute("INSERT INTO clients (name, phone, email) VALUES (?, ?, ?)",
                       (client.name, client.phone, client.email))
        self.conn.commit()
        client.id = cursor.lastrowid
    except sqlite3.Error as e:
        print("Ошибка при добавлении клиента:", e)

def get_clients(self):
    """
    Извлекает всех клиентов из базы.

    Returns
    -------
    list of Client
        Список клиентов в виде объектов Client.
    """
    cursor = self.conn.cursor()
    cursor.execute("SELECT id, name, phone, email FROM clients")
    rows = cursor.fetchall()
    return [Client(name=row[1], phone=row[2], email=row[3], id=row[0]) for row in rows]

def add_product(self, product):
    """
    Добавляет объект Product в базу данных.

    Parameters
    ----------
    product : Product
        Объект товара.
    """
    cursor = self.conn.cursor()
    try:
        cursor.execute("INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
                       (product.name, product.description, product.price))
        self.conn.commit()
        product.id = cursor.lastrowid
    except sqlite3.Error as e:
        print("Ошибка при добавлении товара:", e)

def get_products(self):
    """
    Извлекает все товары из базы.

    Returns
    -------
    list of Product
        Список товаров в виде объектов Product.
    """
    cursor = self.conn.cursor()
    cursor.execute("SELECT id, name, description, price FROM products")
    rows = cursor.fetchall()
    return [Product(name=row[1], description=row[2], price=row[3], id=row[0]) for row in rows]

def add_order(self, order):
    """
    Добавляет заказ (Order или SpecialOrder) и его детали в базу.

    Parameters
    ----------
    order : Order or SpecialOrder
        Объект заказа.
    """
    cursor = self.conn.cursor()
    try:
        discount = getattr(order, "discount", 0)
        cursor.execute("INSERT INTO orders (order_date, client_id, discount) VALUES (?, ?, ?)",
                       (order.order_date, order.client.id, discount))
        self.conn.commit()
        order.id = cursor.lastrowid
        for product, qty in order.products:
            cursor.execute("""INSERT INTO order_details (order_id, product_id, quantity, price)
                              VALUES (?, ?, ?, ?)""",
                           (order.id, product.id, qty, product.price))
        self.conn.commit()
    except sqlite3.Error as e:
        print("Ошибка при добавлении заказа:", e)

def get_orders(self):
    """
    Извлекает заказы, соединяя информацию о клиенте.

    Returns
    -------
    list of tuple
        Кортеж (order_id, order_date, client_name, discount) для каждого заказа.
    """
    cursor = self.conn.cursor()
    cursor.execute("""
        SELECT orders.id, orders.order_date, clients.name, orders.discount
        FROM orders
        LEFT JOIN clients ON orders.client_id = clients.id
    """)
    return cursor.fetchall()

def export_clients_csv(self, filepath):
    """
    Экспортирует список клиентов в CSV-файл.

    Parameters
    ----------
    filepath : str
        Путь к CSV файлу.
    """
    clients = self.get_clients()
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "phone", "email"])
            for client in clients:
                writer.writerow([client.id, client.name, client.phone, client.email])
    except Exception as e:
        print("Ошибка экспорта CSV:", e)

def export_clients_json(self, filepath):
    """
    Экспортирует список клиентов в JSON-файл.

    Parameters
    ----------
    filepath : str
        Путь к JSON файлу.
    """
    clients = self.get_clients()
    clients_data = [{"id": client.id, "name": client.name,
                     "phone": client.phone, "email": client.email} for client in clients]
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(clients_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Ошибка экспорта JSON:", e)

def import_clients_csv(self, filepath):
    """
    Импортирует клиентов из CSV-файла.

    Parameters
    ----------
    filepath : str
        Путь к CSV файлу.
    """
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                client = Client(name=row["name"], phone=row["phone"], email=row["email"])
                self.add_client(client)
    except Exception as e:
        print("Ошибка импорта CSV:", e)

def import_clients_json(self, filepath):
    """
    Импортирует клиентов из JSON-файла.

    Parameters
    ----------
    filepath : str
        Путь к JSON файлу.
    """
    try:
        with open(filepath, encoding="utf-8") as f:
            clients_data = json.load(f)
            for data in clients_data:
                client = Client(name=data["name"], phone=data["phone"], email=data["email"])
                self.add_client(client)
    except Exception as e:
        print("Ошибка импорта JSON:", e)