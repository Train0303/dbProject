DROP TABLE IF EXISTS delivery_area_tb;
DROP TABLE IF EXISTS account_record_tb;
DROP TABLE IF EXISTS account_tb;
DROP TABLE IF EXISTS auction_record_tb;
DROP TABLE IF EXISTS delivery_tb;
DROP TABLE IF EXISTS auction_tb;
DROP TABLE IF EXISTS product_tb;
DROP TABLE IF EXISTS member_tb;
DROP TABLE IF EXISTS member_request_tb;
DROP TABLE IF EXISTS location_tb;
DROP TABLE IF EXISTS employee_tb;
DROP TABLE IF EXISTS employee_request_tb;

DROP FUNCTION IF EXISTS check_auction_validation;
DROP FUNCTION IF EXISTS check_auction_record_validation;
DROP FUNCTION IF EXISTS check_id_in_member;
DROP FUNCTION IF EXISTS check_id_in_employee;

DROP TRIGGER IF EXISTS auction_price_increase_trigger ON auction_tb;
DROP TRIGGER IF EXISTS check_id_in_member_trigger ON member_request_tb;
DROP TRIGGER IF EXISTS check_id_in_employee_trigger ON employee_request_tb;
DROP TRIGGER IF EXISTS check_auction_record_validation_trigger ON auction_record_tb;

DROP ROLE IF EXISTS ROLE_MANAGER;
DROP ROLE IF EXISTS ROLE_CS;
DROP ROLE IF EXISTS ROLE_BUYER;
DROP ROLE IF EXISTS ROLE_SELLER;
DROP ROLE IF EXISTS ROLE_DELIVER;
DROP ROLE IF EXISTS TEMP_ACCOUNT;
DROP USER IF EXISTS manager;
DROP USER IF EXISTS cs;
DROP USER IF EXISTS buyer;
DROP USER IF EXISTS seller;
DROP USER IF EXISTS deliver;

CREATE TABLE member_tb (
    id      VARCHAR(100) PRIMARY KEY,
    name    VARCHAR(30)  NOT NULL,
    pw      VARCHAR(255) NOT NULL,
    role    VARCHAR(20)  NOT NULL CHECK (role = 'role_buyer' OR role = 'role_seller' OR role = 'role_deliver')
);

CREATE TABLE member_request_tb(
    id      VARCHAR(100)    PRIMARY KEY,
    name    VARCHAR(30)     NOT NULL,
    pw      VARCHAR(255)    NOT NULL,
    role    VARCHAR(20)     NOT NULL CHECK (role = 'role_buyer' OR role = 'role_seller' OR role = 'role_deliver')
);

CREATE TABLE location_tb (
    id      BIGSERIAL	 PRIMARY KEY,
    name    VARCHAR(30)  NOT NULL
);

CREATE TABLE delivery_area_tb(
    mem_id  VARCHAR(100) NOT NULL,
    loc_id  BIGINT       NOT NULL,

    FOREIGN KEY (mem_id) REFERENCES member_tb(id),
    FOREIGN KEY (loc_id) REFERENCES location_tb(id),
    PRIMARY KEY (mem_id, loc_id)
);

CREATE TABLE account_tb(
    account_num VARCHAR(20)  PRIMARY KEY,
    mem_id      VARCHAR(100) NOT NULL,
    balance     BIGINT   	 NOT NULL CHECK (balance >= 0)
);

CREATE TABLE account_record_tb(
    id          BIGSERIAL	PRIMARY KEY,
    account_num VARCHAR(20) NOT NULL,
    sender      VARCHAR(20),
    money       BIGINT      NOT NULL,

    FOREIGN KEY (account_num) REFERENCES account_tb(account_num),
    FOREIGN KEY (sender) REFERENCES account_tb(account_num)
);

CREATE TABLE product_tb(
    id          BIGSERIAL	    PRIMARY KEY,
    name        VARCHAR(50)     NOT NULL,
    kind        VARCHAR(50)     NOT NULL,
    description VARCHAR(65535)
);

CREATE TABLE employee_tb(
    id          VARCHAR(100)    PRIMARY KEY,
    name        VARCHAR(30)     NOT NULL,
    pw          VARCHAR(255)    NOT NULL,
    role        VARCHAR(20)     NOT NULL CHECK (role = 'role_manager' OR role = 'role_cs')
    
);

CREATE TABLE employee_request_tb(
    id          VARCHAR(100)    PRIMARY KEY,
    name        VARCHAR(30)     NOT NULL,
    pw          VARCHAR(255)    NOT NULL,
    role        VARCHAR(20)     NOT NULL CHECK (role = 'role_manager' OR role = 'role_cs')
);

CREATE TABLE auction_tb(
    id              BIGSERIAL	    PRIMARY KEY,
    sel_id          VARCHAR(100)    NOT NULL,
    buy_id          VARCHAR(100)    ,
    emp_id          VARCHAR(100)    ,
    product_id      BIGINT          NOT NULL,
    price           BIGINT   	    NOT NULL CHECK (price > 0),
    status          VARCHAR(10)     NOT NULL CHECK (status = 'NOT_READY' or status = 'READY' or status = 'START' or status = 'END'),
    count           INT   	        NOT NULL CHECK (count > 0),
    start_time      TIMESTAMP       NOT NULL,
    end_time        TIMESTAMP       NOT NULL CHECK(end_time > start_time),

    FOREIGN KEY (sel_id) REFERENCES member_tb(id),
    FOREIGN KEY (buy_id) REFERENCES member_tb(id),
    FOREIGN KEY (emp_id) REFERENCES employee_tb(id),
    FOREIGN KEY (product_id) REFERENCES product_tb(id)
);

CREATE TABLE auction_record_tb(
    id          BIGSERIAL	    PRIMARY KEY,
    buy_id      VARCHAR(100)    NOT NULL,
    auc_id      BIGINT          NOT NULL,
    price       BIGINT          NOT NULL CHECK (price > 0),
    order_time  TIMESTAMP       ,

    FOREIGN KEY (buy_id) REFERENCES member_tb(id),
    FOREIGN KEY (auc_id) REFERENCES auction_tb(id)
);

CREATE TABLE delivery_tb(
    auc_id      BIGINT  	    NOT NULL,
    dist_id     VARCHAR(100)    NOT NULL,
    dest        VARCHAR(200)    NOT NULL,
    time_limit  TIMESTAMP       NOT NULL,
    status      VARCHAR(20)     NOT NULL,

    FOREIGN KEY (auc_id) REFERENCES auction_tb(id),
    FOREIGN KEY (dist_id) REFERENCES member_tb(id),
    PRIMARY KEY (auc_id, dist_id)
);


DO
$$
BEGIN
    IF NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'role_manager') THEN
        CREATE ROLE ROLE_MANAGER WITH CREATEROLE INHERIT;
    END IF;

    IF NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'role_cs') THEN
        CREATE ROLE ROLE_CS;
    END IF;

    IF NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'role_buyer') THEN
        CREATE ROLE ROLE_BUYER;
    END IF;

    IF NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'role_seller') THEN
        CREATE ROLE ROLE_SELLER;
    END IF;

    IF NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'role_deliver') THEN
        CREATE ROLE ROLE_DELIVER;
    END IF;

    IF NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'temp_account') THEN
        CREATE ROLE TEMP_ACCOUNT WITH LOGIN PASSWORD '';
    END IF;

    IF NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'manager') THEN
        CREATE USER manager PASSWORD 'qwer1234';
        GRANT role_manager TO manager;
    END IF;

    IF NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'cs') THEN
        CREATE USER cs PASSWORD 'qwer1234';
        GRANT role_cs TO cs;
    END IF;

    IF NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'seller') THEN
        CREATE USER seller PASSWORD 'qwer1234';
        GRANT role_seller TO seller;
    END IF;

    IF NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'buyer') THEN
        CREATE USER buyer PASSWORD 'qwer1234';
        GRANT role_buyer TO buyer;
    END IF;

    IF NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'deliver') THEN
        CREATE USER deliver PASSWORD 'qwer1234';
        GRANT role_deliver TO deliver;
    END IF;
END
$$
;


GRANT INSERT ON TABLE member_request_tb TO TEMP_ACCOUNT;
GRANT INSERT ON TABLE employee_request_tb TO TEMP_ACCOUNT;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to ROLE_CS;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to ROLE_MANAGER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to ROLE_SELLER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to ROLE_BUYER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to ROLE_DELIVER;
INSERT INTO employee_tb values
('manager', 'qwer1234', '매니저', 'role_manager'),
('cs', 'qwer1234', '고객서비스', 'role_cs');

INSERT INTO member_tb values
('seller', 'qwer1234', '판매자', 'role_seller'),
('buyer', 'qwer1234', '구매자', 'role_buyer'),
('deliver', 'qwer1234', '운송업자', 'role_deliver');


CREATE OR REPLACE FUNCTION check_auction_validation()
RETURNS TRIGGER AS $$
BEGIN
    -- Check Auction Price monoton increasing
    IF NEW.price IS DISTINCT FROM OLD.price THEN
        IF NEW.price <= OLD.price THEN
            RAISE EXCEPTION 'New order amount must be greater than the old order amount.';
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_auction_record_validation()
RETURNS TRIGGER AS $$
DECLARE
    start_time_var   TIMESTAMP;
    end_time_var     TIMESTAMP;
BEGIN
    -- Check order_time Not Input
    IF NEW.order_time IS NOT NULL THEN
        RAISE EXCEPTION 'order_time is always null input.';
    END IF;

    NEW.order_time = CURRENT_TIMESTAMP;
    SELECT start_time, end_time INTO start_time_var, end_time_var FROM auction_tb WHERE id = NEW.auc_id;

    -- Check Auction Record Create Time < Auction End Time
    IF CURRENT_TIMESTAMP < start_time_var THEN
        RAISE EXCEPTION 'Not Start Auction.';
    ELSIF CURRENT_TIMESTAMP > end_time_var THEN
        RAISE EXCEPTION 'Already Closing Auction.'; 
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION check_id_in_member()
RETURNS TRIGGER AS $$
DECLARE
    member_id VARCHAR(100);
BEGIN
    SELECT id INTO member_id FROM member_tb WHERE member_tb.id = NEW.id;

    IF count(member_id) > 0 THEN
        RAISE EXCEPTION 'Already Id in Member!';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION check_id_in_employee()
RETURNS TRIGGER AS $$
DECLARE
    employee_id VARCHAR(100);
BEGIN
    SELECT id INTO employee_id FROM employee_tb WHERE id = NEW.id;

    IF count(employee_id) > 0 THEN
        RAISE EXCEPTION 'Already Id in Member!';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;


CREATE TRIGGER auction_price_increase_trigger
BEFORE UPDATE ON auction_tb
FOR EACH ROW
EXECUTE FUNCTION check_auction_price_increase();

CREATE TRIGGER check_id_in_member_trigger
BEFORE INSERT ON member_request_tb
FOR EACH ROW
EXECUTE FUNCTION check_id_in_member();

CREATE TRIGGER check_id_in_employee_trigger
BEFORE INSERT ON employee_request_tb
FOR EACH ROW
EXECUTE FUNCTION check_id_in_employee();

CREATE TRIGGER check_auction_record_validation_trigger
BEFORE INSERT ON auction_record_tb
FOR EACH ROW
EXECUTE FUNCTION check_auction_record_validation();