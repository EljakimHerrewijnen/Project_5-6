CREATE TABLE address (
 postal_code CHAR(6) NOT NULL,
 house_number INT NOT NULL,
 country CHAR(25),
 city CHAR(25),
 PRIMARY KEY(postal_code, house_number)
);

CREATE TABLE product (
 product_id INT NOT NULL PRIMARY KEY,
 name CHAR(25),
 description CHAR(2047),
 price FLOAT(25),
 origin CHAR(25),
 roast_level CHAR(25)
);

CREATE TABLE product_aroma (
 product_id INT NOT NULL,
 name CHAR(15) NOT NULL,
 PRIMARY KEY(product_id, name),
 FOREIGN KEY (product_id) REFERENCES product (product_id)
);

CREATE TABLE wishes (
 product_id INT NOT NULL,
 username char(15) NOT NULL,
 PRIMARY KEY(username, product_id),
 FOREIGN KEY (product_id) REFERENCES product (product_id)
);

CREATE TABLE account (
 username CHAR(15) NOT NULL PRIMARY KEY,
 password CHAR(25),
 name CHAR(20),
 surname CHAR(25),
 birth_date CHAR(10),
 email CHAR(50),
 banned INT,
 register_date CHAR(10),
 account_type CHAR(15),
 wishlist_public INT,
 postal_code CHAR(6),
 house_number INT,
 FOREIGN KEY (postal_code,house_number) REFERENCES address (postal_code,house_number)
);

CREATE TABLE favorites (
 username CHAR(15) NOT NULL,
 product_id INT NOT NULL,
 PRIMARY KEY(username, product_id),
 FOREIGN KEY (username) REFERENCES account (username),
 FOREIGN KEY (product_id) REFERENCES product (product_id)
);

CREATE TABLE orders (
 orders_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 username CHAR(15) NOT NULL,
 orders_date CHAR(10),
 FOREIGN KEY (username) REFERENCES account (username)
);

CREATE TABLE order_details (
 orders_id INT NOT NULL,
 product_id INT NOT NULL,
 quantity INT,
 PRIMARY KEY(orders_id, product_id),
 FOREIGN KEY (orders_id) REFERENCES orders (orders_id),
 FOREIGN KEY (product_id) REFERENCES product (product_id)
);
