""" Модуль gui.py Содержит графический интерфейс с использованием tkinter для работы с клиентами и заказами. """

import tkinter as tk from tkinter import ttk, messagebox, filedialog from datetime import datetime from db import Database from models import Client, Product, Order, SpecialOrder

class MainGUI(tk.Tk): """ Главное окно графического интерфейса. """ def init(self, db): super().init() self.db = db self.title("Система учёта заказов и клиентов") self.geometry("900x600") self.create_menu() self.create_widgets()

def create_menu(self):
    """Создаёт меню приложения."""
    menubar = tk.Menu(self)

    # Меню для клиентов
    client_menu = tk.Menu(menubar, tearoff=0)
    client_menu.add_command(label="Добавить клиента", command=self.open_add_client)
    client_menu.add_command(label="Просмотреть клиентов", command=self.load_clients)
    menubar.add_cascade(label="Клиенты", menu=client_menu)

    # Меню для заказов
    order_menu = tk.Menu(menubar, tearoff=0)
    order_menu.add_command(label="Создать заказ", command=self.open_create_order)
    order_menu.add_command(label="Просмотреть заказы", command=self.load_orders)
    menubar.add_cascade(label="Заказы", menu=order_menu)

    # Меню для импорта/экспорта
    ie_menu = tk.Menu(menubar, tearoff=0)
    ie_menu.add_command(label="Экспорт клиентов в CSV", command=self.export_clients_csv)
    ie_menu.add_command(label="Экспорт клиентов в JSON", command=self.export_clients_json)
    ie_menu.add_separator()
    ie_menu.add_command(label="Импорт клиентов из CSV", command=self.import_clients_csv)
    ie_menu.add_command(label="Импорт клиентов из JSON", command=self.import_clients_json)
    menubar.add_cascade(label="Импорт/Экспорт", menu=ie_menu)

    self.config(menu=menubar)

def create_widgets(self):
    """Создаёт основные элементы интерфейса."""
    self.notebook = ttk.Notebook(self)
    self.notebook.pack(fill="both", expand=True)

    # Вкладка клиентов
    self.clients_frame = ttk.Frame(self.notebook)
    self.notebook.add(self.clients_frame, text="Клиенты")
    self.clients_tree = ttk.Treeview(self.clients_frame,
                                     columns=("id", "name", "phone", "email"),
                                     show="headings")
    for col, heading in zip(("id", "name", "phone", "email"),
                              ("ID", "Имя", "Телефон", "Email")):
        self.clients_tree.heading(col, text=heading)
    self.clients_tree.pack(fill="both", expand=True)

    # Вкладка заказов
    self.orders_frame = ttk.Frame(self.notebook)
    self.notebook.add(self.orders_frame, text="Заказы")
    self.orders_tree = ttk.Treeview(self.orders_frame,
                                    columns=("id", "date", "client", "discount"),
                                    show="headings")
    for col, heading in zip(("id", "date", "client", "discount"),
                              ("ID", "Дата", "Клиент", "Скидка")):
        self.orders_tree.heading(col, text=heading)
    self.orders_tree.pack(fill="both", expand=True)

def open_add_client(self):
    """Открывает окно для добавления клиента."""
    window = tk.Toplevel(self)
    window.title("Добавить клиента")
    window.geometry("300x250")

    tk.Label(window, text="Имя:").pack(pady=5)
    name_entry = tk.Entry(window)
    name_entry.pack(pady=5)
    tk.Label(window, text="Телефон:").pack(pady=5)
    phone_entry = tk.Entry(window)
    phone_entry.pack(pady=5)
    tk.Label(window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(window)
    email_entry.pack(pady=5)

    def save_client():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        client = Client(name, phone, email)
        if not client.validate():
            messagebox.showerror("Ошибка", "Некорректный email или телефон!")
            return
        self.db.add_client(client)
        messagebox.showinfo("Успех", f"Клиент {client.name} добавлен.")
        window.destroy()
        self.load_clients()

    tk.Button(window, text="Сохранить", command=save_client).pack(pady=10)

def load_clients(self):
    """Загружает список клиентов из базы в таблицу."""
    for item in self.clients_tree.get_children():
        self.clients_tree.delete(item)
    clients = self.db.get_clients()
    for client in clients:
        self.clients_tree.insert("", "end", values=(client.id, client.name, client.phone, client.email))

def open_create_order(self):
    """Открывает окно для создания заказа."""
    window = tk.Toplevel(self)
    window.title("Создать заказ")
    window.geometry("400x400")

    # Выбор клиента
    tk.Label(window, text="Выберите клиента:").pack(pady=5)
    clients = self.db.get_clients()
    client_var = tk.StringVar()
    client_options = {f"{cl.id} - {cl.name}": cl for cl in clients}
    client_menu = ttk.Combobox(window, values=list(client_options.keys()), textvariable=client_var)
    client_menu.pack(pady=5)

    # Выбор товара
    tk.Label(window, text="Выберите товар:").pack(pady=5)
    products = self.db.get_products()
    product_var = tk.StringVar()
    product_options = {f"{pr.id} - {pr.name}": pr for pr in products}
    product_menu = ttk.Combobox(window, values=list(product_options.keys()), textvariable=product_var)
    product_menu.pack(pady=5)

    tk.Label(window, text="Количество:").pack(pady=5)
    qty_entry = tk.Entry(window)
    qty_entry.pack(pady=5)

    # Ввод скидки для специального заказа
    tk.Label(window, text="Скидка (%), если есть:").pack(pady=5)
    discount_entry = tk.Entry(window)
    discount_entry.pack(pady=5)

    def create_order():
        try:
            selected_client = client_options[client_var.get()]
            selected_product = product_options[product_var.get()]
            qty = int(qty_entry.get())
            discount_text = discount_entry.get().strip()
            discount = float(discount_text) if discount_text else 0.0
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            products_list = [(selected_product, qty)]
            # Если указана скидка – формируем SpecialOrder, иначе обычный Order.
            if discount > 0:
                order = SpecialOrder(selected_client, products_list, order_date, discount)
            else:
                order = Order(selected_client, products_list, order_date)
            self.db.add_order(order)
            messagebox.showinfo("Успех", f"Заказ создан для клиента {selected_client.name}")
            window.destroy()
            self.load_orders()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать заказ: {e}")

    tk.Button(window, text="Сохранить заказ", command=create_order).pack(pady=10)

def load_orders(self):
    """Загружает список заказов из базы в таблицу."""
    for item in self.orders_tree.get_children():
        self.orders_tree.delete(item)
    orders = self.db.get_orders()
    for order in orders:
        self.orders_tree.insert("", "end", values=order)

def export_clients_csv(self):
    """Экспортирует клиентов в CSV файл."""
    filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
    if filepath:
        self.db.export_clients_csv(filepath)
        messagebox.showinfo("Экспорт", "Данные экспортированы в CSV.")

def export_clients_json(self):
    """Экспортирует клиентов в JSON файл."""
    filepath = filedialog.asksaveasfilename(defaultextension=".json",
                                            filetypes=[("JSON files", "*.json")])
    if filepath:
        self.db.export_clients_json(filepath)
        messagebox.showinfo("Экспорт", "Данные экспортированы в JSON.")

def import_clients_csv(self):
    """Импортирует клиентов из CSV файла."""
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        self.db.import_clients_csv(filepath)
        messagebox.showinfo("Импорт", "Клиенты импортированы из CSV.")
        self.load_clients()

def import_clients_json(self):
    """Импортирует клиентов из JSON файла."""
    filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if filepath:
        self.db.import_clients_json(filepath)
        messagebox.showinfo("Импорт", "Клиенты импортированы из JSON.")
        self.load_clients()