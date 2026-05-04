INSERT INTO raw.brands (name, country) VALUES
('Montale', 'France'),
('Mancera', 'France'),
('Nishane', 'Turkey'),
('By Kilian', 'France'),
('Xerjoff', 'Italy'),
('Mind Games', 'USA'),
('Tiziana Terenzi', 'Italy'),
('BDK Parfums', 'France'),
('Maison Francis Kurkdjian', 'France'),
('Maison Margiela', 'France');

-- Perfumes
INSERT INTO raw.perfumes (brand_id, name, perfume_type, size_ml, price) VALUES
(1, 'Arabians Tonka', 'EDP', 100, 140.00),
(1, 'Roses Musk', 'EDP', 100, 130.00),
(1, 'Intense Cafe', 'EDP', 100, 130.00),
(1, 'Infinity', 'EDP', 100, 140.00),
(2, 'Cedrat Boise', 'EDP', 120, 160.00),
(2, 'Red Tobacco', 'EDP', 120, 170.00),
(2, 'Amore Caffe', 'EDP', 120, 155.00),
(2, 'Amberful', 'EDP', 120, 170.00),
(3, 'Hacivat', 'Extrait de Parfum', 100, 395.00),
(3, 'Ani', 'Extrait de Parfum', 100, 375.00),
(3, 'Tempfluo', 'Extrait de Parfum', 50, 280.00),
(3, 'Wulong Cha', 'Extrait de Parfum', 50, 110.00),
(4, 'Angels'' Share', 'EDP', 100, 415.00),
(4, 'Black Phantom', 'EDP', 50, 230.00),
(4, 'Apple Brandy On The Rocks', 'EDP', 100, 375.00),
(4, 'Old Fashioned', 'EDP', 100, 375.00),
(5, 'Erba Pura', 'EDP', 100, 269.85),
(5, 'Naxos', 'EDP', 100, 400.70),
(5, 'Torino 21', 'EDP', 100, 482.47),
(5, 'Alexandria II', 'EDP', 50, 531.54),
(6, 'Blockade', 'Extrait de Parfum', 100, 395.00),
(6, 'Double Attack', 'Extrait de Parfum', 100, 395.00),
(6, 'French Defense', 'Extrait de Parfum', 100, 395.00),
(6, 'Lionora', 'Extrait de Parfum', 100, 395.00),
(7, 'Kirke', 'Extrait de Parfum', 100, 220.00),
(7, 'Ilba', 'Extrait de Parfum', 100, 220.00),
(7, 'Cubia', 'Extrait de Parfum', 100, 575.00),
(7, 'Atlantide', 'Extrait de Parfum', 100, 850.00),
(8, 'Gris Charnel', 'EDP', 100, 225.00),
(8, 'Rouge Smoking', 'EDP', 100, 225.00),
(8, 'Vanille Caviar', 'EDP', 100, 225.00),
(8, 'Velvet Tonka', 'EDP', 100, 225.00),
(9, 'Baccarat Rouge 540', 'EDP', 70, 265.00),
(9, 'Oud Satin Mood', 'Extrait de Parfum', 70, 360.00),
(9, '724', 'EDP', 70, 205.00),
(9, 'Grand Soir', 'EDP', 70, 205.00),
(10, 'By the Fireplace', 'EDT', 100, 170.00),
(10, 'Jazz Club', 'EDT', 100, 170.00),
(10, 'Lazy Sunday Morning', 'EDT', 100, 170.00),
(10, 'Up At Dawn', 'EDT', 100, 170.00);

-- Locations
INSERT INTO raw.locations (name, state) VALUES
('United States', 'New York'),
('Canada', 'Ottawa'),
('Canada', 'Montreal'),
('United States', 'Florida');

-- Customers
INSERT INTO raw.customers (first_name, last_name, email, location_id) VALUES
('John', 'Smith', 'johnsmith2598@gmail.com', 1),
('Mac', 'Callahan', 'maccallahan1997@gmail.com', 2),
('Albert', 'Roy', 'royalbert12@gmail.com', 3),
('Cristian', 'Valdez', 'valdezcristian10@gmail.com', 4);

-- Sales
INSERT INTO raw.sales (customer_id, perfume_id, location_id, quantity, sale_date) VALUES
(1, 6, 1, 1, '2026-04-10 10:00:14'),
(2, 8, 1, 2, '2026-04-11 11:30:50'),
(1, 11, 2, 1, '2026-04-11 15:42:08'),
(3, 14, 3, 1, '2026-04-12 12:04:02'),
(4, 17, 2, 1, '2026-04-12 18:27:32'),
(1, 21, 1, 1, '2026-04-13 09:15:00'),
(2, 25, 3, 1, '2026-04-13 14:29:00');