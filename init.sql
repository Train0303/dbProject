DO
$$
BEGIN
    IF NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'role_manager') THEN
        CREATE ROLE ROLE_MANAGER  WITH LOGIN PASSWORD 'manager12!';
    END IF;

    IF NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'role_cs') THEN
        create role ROLE_CS WITH LOGIN PASSWORD 'cs12!';
    END IF;

    IF NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'temp_account') THEN
        create role TEMP_ACCOUNT WITH LOGIN PASSWORD '';
    END IF;
END
$$
;


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

CREATE TABLE member_tb (
    id      VARCHAR(100) PRIMARY KEY,
    name    VARCHAR(30)  NOT NULL,
    pw      VARCHAR(255) NOT NULL
);

CREATE TABLE member_request_tb(
    id          VARCHAR(100)    PRIMARY KEY,
    name        VARCHAR(30)     NOT NULL,
    pw          VARCHAR(255)    NOT NULL
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
    role        VARCHAR(20)     NOT NULL
);

CREATE TABLE employee_request_tb(
    id          VARCHAR(100)    PRIMARY KEY,
    name        VARCHAR(30)     NOT NULL,
    pw          VARCHAR(255)    NOT NULL
);

CREATE TABLE auction_tb(
    id              BIGSERIAL	    PRIMARY KEY,
    sel_id          VARCHAR(100)    NOT NULL,
    buy_id          VARCHAR(100)    NOT NULL,
    emp_id          VARCHAR(100)    NOT NULL,
    product_id      BIGINT          NOT NULL,
    price           BIGINT   	    NOT NULL CHECK (price > 0),
    status          VARCHAR(10)     NOT NULL,
    count           INT   	        NOT NULL CHECK (count > 0),
    register_time   TIMESTAMP       NOT NULL,

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
    order_time  TIMESTAMP       NOT NULL,

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

GRANT INSERT ON TABLE member_request_tb TO TEMP_ACCOUNT;
GRANT INSERT ON TABLE employee_request_tb TO TEMP_ACCOUNT;
GRANT ALL PRIVILEGES ON DATABASE dbproject TO ROLE_CS;
GRANT ALL PRIVILEGES ON DATABASE dbproject TO ROLE_MANAGER;

CREATE OR REPLACE FUNCTION check_auction_price_increase()
RETURNS TRIGGER AS $$
BEGIN
    -- 경매가격이 변경되었는지 확인
    IF NEW.price IS DISTINCT FROM OLD.price THEN
        -- 새로운 값이 이전 값보다 큰지 확인
        IF NEW.price <= OLD.price THEN
            RAISE EXCEPTION 'New order amount must be greater than the old order amount.';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

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