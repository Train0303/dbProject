-- member_tb
insert into member_tb (id, name, pw, role) values 
    (4, 'buy4', 'buy4', 'role_buyer'),
    (5, 'buy5', 'buy5', 'role_buyer'),
    (6, 'buy6', 'buy6', 'role_buyer');

-- location_tb
insert into location_tb (id, name) values 
    (1, 'pusan'), (2, 'deagu'), (3, 'soeul');

-- delivery_area_tb
insert into delivery_area_tb (mem_id, loc_id) values 
    (4, 1), (5, 2), (6, 3);

-- account_tb
insert into account_tb (account_num, mem_id, balance) values 
    (1, 1, 10), (2, 2, 20), (3, 3, 30), 
    (4, 4, 40), (5, 5, 50), (6, 6, 60);

-- product_tb
insert into product_tb (id, name, kind, description) values 
    (1, 'product1', 'kind1', 'des1'),
    (2, 'product2', 'kind2', 'des2'), 
    (3, 'product3', 'kind3', 'des3'),
    (4, 'product4', 'kind4', 'des4'), 
    (5, 'product5', 'kind5', 'des5'),
    (6, 'product6', 'kind6', 'des6');