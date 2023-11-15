import json
import psycopg2
from config import config


def main():
    script_file = 'fill_db.sql'
    json_file = 'suppliers.json'

    db_name = input("Введите название новой базы данных: ")
    params = config()

    if database_exists(params, db_name):
        print(f"БД {db_name} уже существует. Отказ в создании дубликата базы данных.")
        return

    create_database(params, db_name)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    conn = None

    try:
        # Подключаемся к созданной базе данных
        with psycopg2.connect(**params) as conn:
            conn.autocommit = True  # Включаем автоматическое подтверждение транзакций
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")

                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")

                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")

                add_foreign_keys(cur)
                print("FOREIGN KEY успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def database_exists(params, db_name):
    """Проверяет, существует ли база данных с указанным именем."""
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
            return cur.fetchone() is not None


def create_database(params, db_name):
    """Создает новую базу данных."""
    # Подключаемся к шаблонной базе данных (template1) без использования блока транзакции
    params.update({'dbname': 'template1'})
    conn = psycopg2.connect(**params)
    conn.autocommit = True  # Включаем автоматическое подтверждение транзакций

    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE {db_name};")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def execute_sql_script(cur, script_file):
    """Выполняет скрипт из файла для заполнения БД данными."""
    with open(script_file, 'r') as script:
        cur.execute(script.read())


def create_suppliers_table(cur):
    """Создает таблицу suppliers."""
    cur.execute("""
        CREATE TABLE suppliers (
            supplier_id SERIAL PRIMARY KEY,
            company_name VARCHAR(255) NOT NULL,
            contact VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            fax VARCHAR(20),
            homepage VARCHAR(255),
            products JSONB
            -- Добавьте другие поля по необходимости
        );
    """)


def get_suppliers_data(json_file):
    """Извлекает данные о поставщиках из JSON-файла."""
    with open(json_file, 'r') as file:
        return json.load(file)


def insert_suppliers_data(cur, suppliers):
    """Добавляет данные из suppliers в таблицу suppliers."""
    for supplier in suppliers:
        cur.execute("""
            INSERT INTO suppliers 
            (company_name, contact, address, phone, fax, homepage, products) 
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            supplier['company_name'],
            supplier['contact'],
            supplier['address'],
            supplier['phone'],
            supplier['fax'],
            supplier['homepage'],
            json.dumps(supplier['products'])
        ))


def add_foreign_keys(cur):
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
    cur.execute("""
        ALTER TABLE products
        ADD COLUMN supplier_id INTEGER,
        ADD CONSTRAINT fk_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id);
    """)
    # При необходимости добавьте дополнительные действия по связыванию таблиц


if __name__ == '__main__':
    main()
