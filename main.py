import os
import psycopg2
from dotenv import load_dotenv
from tabulate import tabulate
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
query = input("Введите SQL-запрос: ")
if not query.strip().lower().startswith("select"):
    print("Ошибка: разрешены только SELECT-запросы")
    exit()
if "limit" not in query.lower():
    query += " LIMIT 5"
try:
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD)
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    headers = []
    for column in cursor.description:
        headers.append(column[0])
    if len(rows) == 0:
        print("Запрос выполнен успешно.")
        print("Данные не найдены.")
    else:
        print()
        print(tabulate(rows, headers=headers, tablefmt="grid"))

    cursor.close()
    connection.close()

except Exception as error:
    print("Ошибка подключения или выполнения запроса.")
    print(error)
