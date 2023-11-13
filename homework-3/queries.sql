-- 1. Название компании заказчика и ФИО сотрудника, работающего над заказом
--    в городе London, с доставкой от компании United Package.
SELECT customers.company_name, CONCAT(employees.first_name, ' ', employees.last_name) AS employee_name
FROM customers
JOIN orders ON customers.customer_id = orders.customer_id
JOIN employees ON orders.employee_id = employees.employee_id
JOIN shippers ON orders.ship_via = shippers.shipper_id
WHERE customers.city = 'London'
  AND employees.city = 'London'
  AND shippers.company_name = 'United Package';

-- 2. Наименование продукта, количество товара, имя поставщика и его телефон
--    для продуктов, которые не сняты с продажи, < 25, и в категориях Dairy Products и Condiments.
SELECT product_name, units_in_stock, contact_name, phone
FROM products
JOIN categories USING(category_id)
JOIN suppliers USING(supplier_id)
WHERE category_name IN ('Dairy Products', 'Condiments') AND discontinued = 0
AND units_in_stock < 25
ORDER BY units_in_stock;

-- 3. Список компаний заказчиков, не сделавших ни одного заказа.
SELECT customers.company_name
FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id
WHERE orders.order_id IS NULL
ORDER BY customers.company_name;

-- 4. Уникальные названия продуктов, которых заказано ровно 10 единиц
--    (используется подзапрос).
SELECT product_name
FROM products
WHERE product_id = ANY (SELECT product_id FROM order_details WHERE quantity = 10);