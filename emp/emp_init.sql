insert into member_tb (id, name, pw, role) values 
('buy4', 'buy4', 'qwer1234', 'role_buyer'),
('buy5', 'buy5', 'qwer1234', 'role_buyer'),
('seller2', '판매자2', 'qwer1234', 'role_seller'),
('seller3', '판매자3', 'qwer1234', 'role_seller');

CREATE USER buy4 PASSWORD 'qwer1234';
GRANT role_buyer TO buy4;

CREATE USER buy5 PASSWORD 'qwer1234';
GRANT role_buyer TO buy5;

CREATE USER seller2 PASSWORD 'qwer1234';
GRANT role_seller TO seller2;

CREATE USER seller3 PASSWORD 'qwer1234';
GRANT role_seller TO seller3;

INSERT INTO product_tb(name, kind, description) VALUES
('얼음골 사과 1kg 팝니다', '사과', '얼음골 꿀사과 1kg 만원입니다.'),
('나주 배 1kg 팝니다', '배', '유명한 나주 배 1kg 만원에 팝니다!'),
('각 수확한 수박팝니다', '수박', '싱싱한 수박 팝니다!!'),
('올해 수확한 햇쌀 팝니다', '쌀', '올해 수확한 햇쌀 20kg당 2만원에 팝니다.');

INSERT INTO auction_tb(id, sel_id, buy_id, emp_id, product_id, price, verified, count, adjust ,start_time, end_time) VALUES
(1, 'seller', NULL, NULL, 1, 10000, 'Y', 5, 'N', '2023-11-25', '2023-12-29'),
(2, 'seller', NULL, NULL, 2, 10000, 'Y', 2, 'N', '2023-11-29', '2023-12-30'),
(3, 'seller', NULL, NULL, 3, 20000, 'N', 4, 'N', '2023-11-29', '2023-12-25');

INSERT INTO auction_record_tb(id, buy_id, auc_id, price, order_time) VALUES
(1, 'buy4', 1, 15000, NULL),
(2, 'buy5', 1, 20000, NULL);

INSERT INTO account_record_tb(receiver, sender, money) VALUES
('seller', 'buy4', 10000),
('buy4', NULL, -10000),
('buy5', NULL, 10000),
('seller2', 'buy5', 10000);