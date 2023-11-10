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
SELECT products.product_name, products.units_in_stock, suppliers.contact_name, suppliers.phone
FROM products
JOIN suppliers ON products.supplier_id = suppliers.supplier_id
WHERE products.discontinued = 0 -- предполагая, что 0 означает false
  AND products.units_in_stock < 25
  AND products.category_id IN (1, 2) -- ID категорий Dairy Products и Condiments
ORDER BY products.units_in_stock ASC;

-- 3. Список компаний заказчиков, не сделавших ни одного заказа.
SELECT customers.company_name
FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id
WHERE orders.order_id IS NULL
ORDER BY customers.company_name;

-- 4. Уникальные названия продуктов, которых заказано ровно 10 единиц
--    (используется подзапрос).
SELECT DISTINCT products.product_name
FROM products
JOIN order_details ON products.product_id = order_details.product_id
WHERE order_details.quantity = 10;
