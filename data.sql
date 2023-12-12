-- member_tb
insert into member_tb (id, name, pw, balance, role) values 
    ('buy2', 'buy2', 'qwer1234',  400,'role_buyer'),
    ('buy3', 'buy3', 'qwer1234',  500,'role_buyer'),
    ('buy4', 'buy4', 'qwer1234',  600,'role_buyer'),
    ('db2023', 'db2023', 'db2023', 700, 'role_seller'),
    ('seller2', 'seller2', 'qwer1234', 0,'role_seller'),
    ('seller3', 'seller3', 'qwer1234', 0,'role_seller'),
    ('deliver2', 'deliver2', 'qwer1234', 0,'role_deliver');


-- location_tb
insert into location_tb (name) values 
    ('pusan Nam-gu'), ('Pusan Geumjeong-gu'), ('deagu Suseong-gu');

-- delivery_area_tb
insert into delivery_area_tb (mem_id, loc_id) values 
    ('buy2', 1), ('buy3', 2), ('buy4', 3);

-- product_tb
insert into product_tb (name, kind, description) values 
    ('gala apple', 'apple', 'middle size red apple'),
    ('granny smith apple', 'apple', 'green apple'),
    ('Naju pear', 'pear', 'Naju pear big size'),
    ('water melon', 'water melon', 'water melon without seed'),
    ('yellow melon', 'water melon', 'yellow color water melon'),
    ('product2', 'kind2', 'des2'), 
    ('product3', 'kind3', 'des3'),
    ('product4', 'kind4', 'des4'), 
    ('product5', 'kind5', 'des5'),
    ('product6', 'kind6', 'des6');


-- auction_tb
INSERT INTO auction_tb(sel_id, buy_id, emp_id, product_id, price, verified, count, adjust ,start_time, end_time) VALUES
('seller',   NULL,      NULL, 1, 10000, 'Y', 5, 'N', '2023-11-25', '2023-12-29'),
('seller',   NULL,      NULL, 2, 10000, 'Y', 2, 'N', '2023-11-29', '2023-12-30'),
('seller',   NULL,      NULL, 3, 20000, 'Y', 4, 'N', '2023-11-29', '2023-12-25'),
('seller', 'buy3', 'manager', 1, 20000, 'Y', 5, 'Y', '2023-11-25', '2023-12-09'),
('seller',   NULL,      NULL, 2, 10000, 'Y', 2, 'N', '2023-11-29', '2023-12-30'),
('seller',   NULL,      NULL, 3, 20000, 'N', 4, 'N', '2023-11-29', '2023-12-25');

-- auction_record_tb
INSERT INTO auction_record_tb(id, buy_id, auc_id, price, order_time) VALUES
(1, 'buy2', 1, 15000, NULL),
(2, 'buy3', 1, 20000, NULL);

-- account_record_tb
INSERT INTO account_record_tb(receiver, sender, money) VALUES
('seller', 'buy2', 10000),
(NULL, 'buy2', 10000),
('buy3', NULL, 10000),
('seller2', 'buy3', 10000);


-- delivery_tb
INSERT INTO delivery_tb(auc_id, deli_id, loc_id, address, status) VALUES
(1, 'deliver2', 1, 'Daeyeon-dong Nam-gu Office', 'READY'),
(2, 'deliver2', 2, 'Pusan National University cse building', 'IN_PROGRESS'),
(3, 'deliver2', 3, '1 Baseball Jeonseol-ro Samsung Lions Park', 'DELIVERED');


-- create user
CREATE USER buy2 PASSWORD 'qwer1234';
GRANT role_buyer TO buy2;

CREATE USER buy3 PASSWORD 'qwer1234';
GRANT role_buyer TO buy3;

CREATE USER seller2 PASSWORD 'qwer1234';
GRANT role_seller TO seller2;

CREATE USER seller3 PASSWORD 'qwer1234';
GRANT role_seller TO seller3;

CREATE USER deliver2 PASSWORD 'qwer1234';
GRANT role_deliver TO deliver2;






