CREATE TABLE raw.brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100)
);

CREATE TABLE raw.perfumes (
    id SERIAL PRIMARY KEY,
    brand_id INT REFERENCES raw.brands(id),
    name VARCHAR(100) NOT NULL,
    perfume_type VARCHAR(50), -- EDP, EDT, Extrait
    size_ml INT,
    price DECIMAL(10, 2)
);

CREATE TABLE raw.locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    state VARCHAR(100)
);


CREATE TABLE raw.customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(150) UNIQUE, 
    location int REFERENCES raw.locations(id)
);

CREATE TABLE raw.sales (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES raw.customers(id),
    perfume_id INT REFERENCES raw.perfumes(id),
    location_id INT REFERENCES raw.locations(id),
    quantity INT DEFAULT 1,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE raw.inventory (
    id SERIAL PRIMARY KEY,
    perfume_id INT REFERENCES raw.perfumes(id),
    current_stock INT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);