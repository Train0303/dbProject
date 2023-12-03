-- member_tb
insert into member_tb (id, name, pw, balance, role) values 
    (4, 'buy4', 'buy4',  400,'role_buyer'),
    (5, 'buy5', 'buy5',  500,'role_buyer'),
    (6, 'buy6', 'buy6',  600,'role_buyer'),
    ('db2023', 'db2023', 'db2023', 700, 'role_seller');

-- location_tb
insert into location_tb (id, name) values 
    (1, 'pusan'), (2, 'deagu'), (3, 'soeul');

-- delivery_area_tb
insert into delivery_area_tb (mem_id, loc_id) values 
    (4, 1), (5, 2), (6, 3);

-- product_tb
insert into product_tb (id, name, kind, description) values 
    (1, 'product1', 'kind1', 'des1'),
    (2, 'product2', 'kind2', 'des2'), 
    (3, 'product3', 'kind3', 'des3'),
    (4, 'product4', 'kind4', 'des4'), 
    (5, 'product5', 'kind5', 'des5'),
    (6, 'product6', 'kind6', 'des6');

-- auction_tb
INSERT INTO auction_tb(id, sel_id, buy_id, emp_id, product_id, price, verified, count, adjust ,start_time, end_time) VALUES
(1, 'seller', NULL, NULL, 1, 10000, 'Y', 5, 'N', '2023-11-25', '2023-12-29'),
(2, 'seller', NULL, NULL, 2, 10000, 'Y', 2, 'N', '2023-11-29', '2023-12-30'),
(3, 'seller', NULL, NULL, 3, 20000, 'N', 4, 'N', '2023-11-29', '2023-12-25');