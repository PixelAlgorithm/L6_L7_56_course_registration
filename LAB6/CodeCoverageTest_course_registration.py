# Prajwal M - PES2UG24CS910
# Lab 6: Code Coverage Tests

import pytest
from course_registration import can_register, waitlist_position, late_fee


# tests for can_register
def test_can_register_valid_regular():
    # regular student within credit limit
    assert can_register("regular", 16, 4, True) == "registered"

def test_can_register_unknown_status():
    # invalid student status should raise ValueError
    with pytest.raises(ValueError, match="unknown status"):
        can_register("special", 12, 4, True)

def test_can_register_invalid_course_credits():
    # course credits <= 0 should raise ValueError
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 12, 0, True)

def test_can_register_prerequisites_missing():
    # prerequisites not completed
    assert can_register("regular", 12, 4, False) == "prerequisites missing"

def test_can_register_credit_limit_exceeded():
    # total credits exceeding limit
    assert can_register("probation", 14, 4, True) == "credit limit exceeded"


# tests for waitlist_position
def test_waitlist_invalid_capacity():
    # capacity <= 0 should raise ValueError
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, 0, 0)

def test_waitlist_seat_available():
    # seats are still open
    assert waitlist_position(25, 30, 0) == 0

def test_waitlist_full_over_ten():
    # waitlist already reached maximum length of 10
    assert waitlist_position(30, 30, 10) == -1

def test_waitlist_position_increment():
    # next student gets assigned waitlist position
    assert waitlist_position(30, 30, 4) == 5


# tests for late_fee
def test_late_fee_zero_or_negative_days():
    # registered on time or before deadline
    assert late_fee(0, 16, False) == 0

def test_late_fee_with_waiver():
    # fee is waived
    assert late_fee(5, 16, True) == 0

def test_late_fee_within_7_days():
    # flat late fee for first week
    assert late_fee(5, 16, False) == 500

def test_late_fee_after_7_days_with_high_credits_and_cap():
    # fee with daily extra and credit surcharge capped at 2000
    assert late_fee(25, 22, False) == 2000
