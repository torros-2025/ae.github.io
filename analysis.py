""" Модуль analysis.py Содержит функции анализа данных и визуализации с использованием pandas, matplotlib, seaborn и networkx. """

import pandas as pd import matplotlib.pyplot as plt import seaborn as sns import networkx as nx

def top_5_clients(orders_df): """ Определяет топ 5 клиентов по числу заказов.

Parameters
----------
orders_df : pandas.DataFrame
    Датафрейм с данными заказов. Должен иметь столбец 'client'.

Returns
-------
pandas.Series
    Счетчик заказов для топ 5 клиентов.
"""
top_clients = orders_df['client'].value_counts().head(5)
return top_clients
def orders_over_time(orders_df): """ Отображает динамику количества заказов по датам.

Parameters
----------
orders_df : pandas.DataFrame
    Датафрейм с данными заказов. Должен содержать столбец 'order_date'.
"""
orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
orders_df['date'] = orders_df['order_date'].dt.date
orders_count = orders_df.groupby('date').size()
plt.figure(figsize=(10, 5))
sns.lineplot(x=orders_count.index, y=orders_count.values)
plt.xlabel("Дата")
plt.ylabel("Количество заказов")
plt.title("Динамика заказов по датам")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
def build_client_graph(orders_df): """ Строит граф связей клиентов: клиенты соединяются, если их заказы имеют общие товары.

Parameters
----------
orders_df : pandas.DataFrame
    Датафрейм с как минимум двумя столбцами 'client' и 'products',
    где 'products' – строковое представление списка товаров.

Returns
-------
networkx.Graph
    Граф связей между клиентами.
"""
G = nx.Graph()
clients = orders_df['client'].unique()
G.add_nodes_from(clients)
for i, row1 in orders_df.iterrows():
    for j, row2 in orders_df.iterrows():
        if i >= j:
            continue
        prods1 = set(row1['products'].split(','))
        prods2 = set(row2['products'].split(','))
        if prods1.intersection(prods2):
            G.add_edge(row1['client'], row2['client'])
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray")
plt.title("Граф связей клиентов")
plt.show()
return G