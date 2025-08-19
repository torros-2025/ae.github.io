""" Точка входа в проект. """

from db import Database from gui import MainGUI

def main(): """ Инициализирует базу данных и запускает графический интерфейс. """ db = Database("shop.db") # Если база данных пуста, добавим тестовые товары if not db.get_products(): from models import Product db.add_product(Product("Ноутбук", "Описание ноутбука", 75000)) db.add_product(Product("Смартфон", "Описание смартфона", 35000)) app = MainGUI(db) app.mainloop()

if name == "main": main()