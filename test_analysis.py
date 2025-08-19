""" Модуль unit-тестов для функций анализа данных в analysis.py. """

import unittest import pandas as pd from analysis import top_5_clients

class TestAnalysis(unittest.TestCase): def test_top_5_clients(self): data = { "client": ["Алиса", "Боб", "Алиса", "Дмитрий", "Боб", "Боб", "Елена"], "order_date": ["2023-10-01"] * 7, "products": ["Товар1"] * 7 } df = pd.DataFrame(data) top_clients = top_5_clients(df) self.assertEqual(top_clients["Боб"], 3) self.assertEqual(top_clients["Алиса"], 2)

if name == "main": unittest.main()