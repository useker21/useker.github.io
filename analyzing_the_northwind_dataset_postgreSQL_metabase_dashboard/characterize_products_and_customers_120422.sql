--Count the number of products in the products table.
SELECT COUNT(productID) FROM products;

--Count separate numbers for currently available and discontinued products.
SELECT COUNT(productID) FROM products WHERE unitsInStock>0 AND discontinued>0;

--Count which product got ordered how many times.

SELECT productName, SUM(unitsOnOrder) AS sum_of_orders FROM products GROUP BY productName ORDER BY sum_of_orders DESC;

--Calculate the percentage of a product on the total number of orders.

--Verify that the sum of percentages is 100%.

--From the Customers table, retrieve all rows containing your country.

SELECT * FROM customers WHERE country='Germany';