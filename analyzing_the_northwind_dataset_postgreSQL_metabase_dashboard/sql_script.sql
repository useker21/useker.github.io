-- categories
DROP TABLE if exists categories;

CREATE TABLE categories (
    categoryID INT PRIMARY KEY NOT NULL,
    categoryName VARCHAR(30),
    descr VARCHAR(100),
    picture TEXT

);

\COPY categories (categoryID, categoryName, descr, picture) FROM '../data/categories.csv' DELIMITER ',' CSV HEADER;

-- customers

DROP TABLE if exists customers;

CREATE TABLE customers (
    customerID VARCHAR(5) PRIMARY KEY NOT NULL,
    companyName VARCHAR(50),
    contactName VARCHAR(30),
    contactTitle VARCHAR(60),
    addres VARCHAR(50),
    city VARCHAR(30),
    region VARCHAR(60),
    postalCode VARCHAR(50),
    country VARCHAR(50),
    phone VARCHAR(50),
    fax VARCHAR(50)
);

\COPY customers (customerID, companyName, contactName, contactTitle, addres, city, region, postalCode, country, phone, fax) FROM '../data/customers.csv' DELIMITER ',' CSV HEADER;

-- employee_territories

DROP TABLE if exists employee_territories;

CREATE TABLE employee_territories(
    employeeID INT NOT NULL,
    territoryID TEXT NOT NULL

);

\COPY employee_territories (employeeID, territoryID) FROM '..\data\employee_territories.csv' DELIMITER ',' CSV HEADER;

--employees

DROP TABLE if exists employees;

CREATE TABLE employees(
    employeeID INT PRIMARY KEY NOT NULL,
    lastName VARCHAR(30),
    firstName VARCHAR (30),
    title VARCHAR(30),
    titleOfCourtesy VARCHAR(5),
    birthDate TIMESTAMP,
    hireDate TIMESTAMP,
    addres TEXT,
    city VARCHAR(30),
    region VARCHAR(30),
    postalCode VARCHAR(30),
    country VARCHAR(15),
    homePhone VARCHAR(30),
    extension INT,
    photo TEXT,
    notes TEXT,
    reportsTo TEXT,
    photoPath TEXT

);

\COPY employees(employeeID, lastName, firstName, title, titleOfCourtesy, birthDate,hireDate,addres,city,region,postalCode, country, homePhone, extension, photo, notes, reportsTo,photoPath) FROM '..\data\employees.csv' DELIMITER ',' CSV HEADER;

-- order details -- primary key is not exist

DROP TABLE if exists order_details;

CREATE TABLE order_details(
    orderID INT NOT NULL,
    productID INT,
    unitPrice FLOAT,
    quantity INT,
    discount FLOAT

);

\COPY order_details(orderID, productID, unitPrice, quantity, discount) FROM '../data/order_details.csv' DELIMITER ',' CSV HEADER;

--orders

DROP TABLE if exists orders;

CREATE TABLE orders(
    orderID INT PRIMARY KEY NOT NULL,
    customerID VARCHAR(5),
    employeeID INT,
    orderDate TIMESTAMP,
    requiredDate TIMESTAMP,
    shippedDate TIMESTAMP NULL,
    shipVia INT,
    freight FLOAT,
    shipName TEXT,
    shipAddress TEXT,
    shipCity TEXT,
    shipRegion TEXT,
    shipPostalCode VARCHAR(55),
    shipCountry VARCHAR(55)

);

\COPY orders(orderID, customerID, employeeID, orderDate, requiredDate, shippedDate, shipVia, freight, shipName, shipAddress, shipCity, shipRegion, shipPostalCode, shipCountry) FROM '../data/orders.csv' DELIMITER ',' CSV HEADER NULL AS 'NULL';

-- products

DROP TABLE if exists products;

CREATE TABLE products(
    productID INT PRIMARY KEY NOT NULL,
    productName VARCHAR(100),
    supplierID INT,
    categoryID INT,
    quantityPerUnit TEXT,
    unitPrice FLOAT,
    unitsInStock INT,
    unitsOnOrder INT,
    reOrderLevel INT,
    discontinued INT


);
\COPY products (productID, productName, supplierID, categoryID, quantityPerUnit, unitPrice, unitsInStock,unitsOnOrder, reOrderLevel, discontinued) FROM '..\data\products.csv' DELIMITER ',' CSV HEADER;

--regions

DROP TABLE if exists regions;

CREATE TABLE regions(
    regionID INT PRIMARY KEY NOT NULL,
    regionDescription VARCHAR(10)
);

\COPY regions(regionID, regionDescription) FROM '../data/regions.csv' DELIMITER ',' CSV HEADER;

--shippers

DROP TABLE if exists shippers;

CREATE TABLE shippers(
    shipperID INT PRIMARY KEY NOT NULL,
    companyName VARCHAR(30),
    phone TEXT
);

\COPY shippers(shipperID, companyName, phone) FROM '../data/shippers.csv' DELIMITER ',' CSV HEADER;

--suppliers 
 DROP TABLE if exists suppliers;

 CREATE TABLE suppliers(
     supplierID INT PRIMARY KEY NOT NULL,
     companyName TEXT,
     contactName TEXT,
     contactTitle VARCHAR(55),
     addres TEXT,
     city TEXT,
     region TEXT,
     postalCode TEXT,
     country VARCHAR(25),
     phone TEXT,
     fax TEXT,
     homePage TEXT


 );

\COPY suppliers(supplierID, companyName, contactName, contactTitle, addres, city, region, postalCode, country, phone, fax, homePage) FROM '../data/suppliers.csv' DELIMITER ',' CSV HEADER;

--territories

DROP TABLE if exists territories;

CREATE TABLE territories(
    territoryID INT PRIMARY KEY NOT NULL,
    territoryDescription TEXT,
    regionID INT
);

\COPY territories(territoryID, territoryDescription, regionID) FROM '../data/territories.csv' DELIMITER ',' CSV HEADER;

