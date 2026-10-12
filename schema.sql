CREATE DATABASE food_order;
USE food_order;

-- 👤 USERS TABLE
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- 🛠️ ADMIN TABLE
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO admin (username, password)
VALUES ('admin', 'admin123');

-- 🍔 PRODUCTS TABLE
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    image VARCHAR(200)
);

-- SAMPLE PRODUCTS
INSERT INTO products (name, description, price, image) VALUES
('Sandwich', 'Grilled veg sandwich', 80, 'sandwitch.jpg'),
('French Fries', 'Crispy salted fries', 70, 'fries.jpg'),
('Momos', 'Steamed veg momos', 90, 'momo.jpg'),
('Noodles', 'Hakka noodles', 120, 'noodle.jpg'),
('Paneer Tikka', 'Spicy grilled paneer', 180, 'paneer.jpg'),
('Biryani', 'Veg dum biryani', 220, 'biryani.jpg'),
('Cold Coffee', 'Chilled creamy coffee', 100, 'coffee.jpg'),
('Ice Cream', 'Vanilla ice cream scoop', 60, 'icecream.jpg'),
('Dosa', 'Crispy masala dosa', 100, 'dosa.jpg'),
('Samosa', 'Hot crispy samosa', 30, 'samosa.jpg'),
('Yorkshire Lamb Patties', 'Lamb patties, soft and juicy', 280, '1.jpg'),
('Lobster Thermidor', 'French lobster dish', 250, '2.jpg'),
('Chicken Madeira', 'Chicken with wine sauce', 400, '3.jpg'),
('Stuffed Jacket Potatoes', 'Potato with stuffing', 320, '4.jpg'),
('Pink Spaghetti Gamberoni', 'Prawns pasta', 380, '5.jpg');

-- 🛒 CART TABLE
CREATE TABLE cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- 📦 ORDERS TABLE
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 📦 ORDER ITEMS TABLE
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

describe users;