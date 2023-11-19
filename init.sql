DROP TABLE IF EXISTS delivery_area_tb;
DROP TABLE IF EXISTS account_record_tb;
DROP TABLE IF EXISTS account_tb;
DROP TABLE IF EXISTS auction_record_tb;
DROP TABLE IF EXISTS delivery_tb;
DROP TABLE IF EXISTS auction_tb;
DROP TABLE IF EXISTS product_tb;
DROP TABLE IF EXISTS member_tb;
DROP TABLE IF EXISTS location_tb;
DROP TABLE IF EXISTS employee_tb;

CREATE TABLE member_tb (
    id      VARCHAR(100) PRIMARY KEY,
    name    VARCHAR(30)  NOT NULL,
    pw      VARCHAR(255) NOT NULL
);

CREATE TABLE location_tb (
    id      BIGINT       PRIMARY KEY,
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
    id          BIGINT      PRIMARY KEY,
    account_num VARCHAR(20) NOT NULL,
    sender      VARCHAR(20),
    money       BIGINT      NOT NULL,

    FOREIGN KEY (account_num) REFERENCES account_tb(account_num),
    FOREIGN KEY (sender) REFERENCES account_tb(account_num)
);

CREATE TABLE product_tb(
    id          BIGINT          PRIMARY KEY,
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

CREATE TABLE auction_tb(
    id              BIGINT          PRIMARY KEY,
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
    id          BIGINT          PRIMARY KEY,
    buy_id      VARCHAR(100)    NOT NULL,
    auc_id      BIGINT          NOT NULL,
    price       BIGINT          NOT NULL CHECK (price > 0),
    order_time  TIMESTAMP       NOT NULL,

    FOREIGN KEY (buy_id) REFERENCES member_tb(id),
    FOREIGN KEY (auc_id) REFERENCES auction_tb(id)
);

CREATE TABLE delivery_tb(
    auc_id      BIGINT          NOT NULL,
    dist_id     VARCHAR(100)    NOT NULL,
    dest        VARCHAR(200)    NOT NULL,
    time_limit  TIMESTAMP       NOT NULL,
    status      VARCHAR(20)     NOT NULL,

    FOREIGN KEY (auc_id) REFERENCES auction_tb(id),
    FOREIGN KEY (dist_id) REFERENCES member_tb(id),
    PRIMARY KEY (auc_id, dist_id)
);