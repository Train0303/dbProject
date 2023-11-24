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