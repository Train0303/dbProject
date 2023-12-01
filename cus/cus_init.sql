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