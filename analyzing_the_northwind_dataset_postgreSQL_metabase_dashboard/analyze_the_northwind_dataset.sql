--Get the names and the quantities in stock for each product.
SELECT productName, unitsInStock FROM products ORDER BY unitsInStock DESC;

--Get a list of current products (Product ID and name).
SELECT productID, productName FROM products;

--Get a list of the most and least expensive products (name and unit price).
SELECT productname, unitPrice FROM products WHERE unitPrice=(SELECT MIN(unitPrice) FROM products) OR unitPrice=(SELECT MAX(unitPrice) FROM products);

--Get products that cost less than $20.
SELECT productName, unitPrice FROM products WHERE unitPrice<20 ORDER BY unitPrice ASC;

--Get products that cost between $15 and $25.
SELECT productName, unitPrice FROM products WHERE unitPrice BETWEEN 15 AND 25 ORDER BY unitPrice ASC;

--Get products above average price
SELECT productName, unitPrice FROM products WHERE unitPrice>(SELECT AVG(unitPrice) FROM products) ORDER BY unitPrice ASC;

--Find the ten most expensive products.
SELECT productName, unitPrice FROM products ORDER BY unitPrice DESC LIMIT 10;

--Get a list of discontinued products (Product ID and name).
SELECT productName, productID, discontinued FROM products WHERE discontinued=0;

--Count current and discontinued products.
SELECT COUNT(productName) FROM products GROUP BY discontinued;

--Find products with less units in stock than the quantity on order.
SELECT productName, unitsInStock, unitsOnOrder FROM products WHERE unitsInStock<unitsOnOrder;

--Find the customer who had the highest order amount
SELECT SUM(unitPrice*quantity*(1+discount)) AS order_amount, customers.customerID, customers.companyName FROM order_details RIGHT JOIN orders ON order_details.orderID=orders.orderID RIGHT JOIN customers ON orders.customerID=customers.customerID GROUP BY customers.customerID ORDER BY order_amount DESC;

--Get orders for a given employee and the according customer
SELECT employeeID, customerID, orderID FROM orders;

--Find the hiring age of each employee
SELECT lastName, firstName, birthDate, hireDate, DATEDIFF(YEAR, hireDate, birthDate) AS hiring_age FROM employees ORDER BY hiring_age;


