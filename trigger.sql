
CREATE OR REPLACE FUNCTION check_auction_price_increase()
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

-- CREATE OR REPLACE FUNCTION check_auction_validation()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     -- Insert Data Don't have verifed and adjust
--     IF NEW.verified IS NOT NULL OR NEW.adjust IS NOT NULL THEN
--         RAISE EXCEPTION 'Insert Data Don`t have verifed and adjust';
--     END IF;

--     NEW.verified = 'N';
--     NEW.adjust = 'N';
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION check_auction_record_validation()
RETURNS TRIGGER AS $$
DECLARE
    start_time_var   DATE;
    end_time_var     DATE;
    is_verified      CHAR(1);
BEGIN
    -- Check order_time Not Input
    IF NEW.order_time IS NOT NULL THEN
        RAISE EXCEPTION 'order_time is always null input.';
    END IF;

    NEW.order_time = CURRENT_TIMESTAMP;
    SELECT start_time, end_time, verified INTO start_time_var, end_time_var, is_verified FROM auction_tb WHERE id = NEW.auc_id;

    -- Check Verified Auction
    IF is_verified = 'N' THEN
        RAISE EXCEPTION 'NOT VERIFIED Auction';
    END IF;

    -- Check Auction Record Create Time < Auction End Time
    IF NEW.order_time < start_time_var THEN
        RAISE EXCEPTION 'Not Start Auction.';
    ELSIF NEW.order_time > end_time_var THEN
        RAISE EXCEPTION 'Already Closing Auction.'; 
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION check_id_in_member()
RETURNS TRIGGER AS $$
DECLARE
    member_id       VARCHAR(100);
    employee_id     VARCHAR(100);
    emp_request_id  VARCHAR(100);
BEGIN
    SELECT id INTO member_id FROM member_tb WHERE member_tb.id = NEW.id;
    SELECT id INTO employee_id FROM employee_tb WHERE employee_tb.id = NEW.id;
    SELECT id INTO emp_request_id FROM employee_request_tb WHERE employee_request_tb.id = NEW.id;
    
    IF count(member_id) > 0 OR count(employee_id) > 0 OR count(emp_request_id) > 0 THEN
        RAISE EXCEPTION 'Already Id in Member!';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION check_id_in_employee()
RETURNS TRIGGER AS $$
DECLARE
    employee_id     VARCHAR(100);
    member_id       VARCHAR(100);
    mem_request_id  VARCHAR(100);
BEGIN
    SELECT id INTO employee_id FROM employee_tb WHERE id = NEW.id;
    SELECT id INTO member_id FROM member_tb WHERE member_tb.id = NEW.id;
    SELECT id INTO mem_request_id FROM member_request_tb WHERE member_request_tb.id = NEW.id;

    IF count(employee_id) > 0 OR count(member_id) > 0 OR count(mem_request_id) > 0 THEN
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

-- CREATE TRIGGER check_auction_validation_trigger
-- BEFORE INSERT ON auction_tb
-- FOR EACH ROW
-- EXECUTE FUNCTION check_auction_validation();