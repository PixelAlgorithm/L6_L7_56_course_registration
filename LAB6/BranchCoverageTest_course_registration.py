# Prajwal M - PES2UG24CS910
# Lab 6: Branch Coverage Tests

import pytest
from course_registration import can_register, waitlist_position, late_fee


# can_register branch coverage
def test_branch_student_status_invalid():
    # check unknown status branch
    with pytest.raises(ValueError, match="unknown status"):
        can_register("guest", 12, 4, True)

def test_branch_student_status_valid_all_tiers():
    # check valid status branch across all student types
    assert can_register("regular", 12, 4, True) == "registered"
    assert can_register("probation", 10, 4, True) == "registered"
    assert can_register("honors", 20, 4, True) == "registered"

def test_branch_course_credits_invalid_zero_and_negative():
    # check zero and negative credits branch
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 12, 0, True)
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 12, -4, True)

def test_branch_course_credits_valid():
    # check valid course credits branch
    assert can_register("regular", 12, 3, True) == "registered"

def test_branch_prerequisites_missing():
    # check missing prerequisites branch
    assert can_register("regular", 12, 4, False) == "prerequisites missing"

def test_branch_prerequisites_met():
    # check prerequisites satisfied branch
    assert can_register("regular", 12, 4, True) == "registered"

def test_branch_credit_limit_exceeded():
    # check exceeding credit limit branch for all categories
    assert can_register("regular", 22, 4, True) == "credit limit exceeded"
    assert can_register("probation", 14, 4, True) == "credit limit exceeded"
    assert can_register("honors", 26, 4, True) == "credit limit exceeded"

def test_branch_credit_limit_boundary_exact_match():
    # check exact limit boundary branch
    assert can_register("regular", 20, 4, True) == "registered"
    assert can_register("probation", 12, 4, True) == "registered"
    assert can_register("honors", 24, 4, True) == "registered"


# waitlist_position branch coverage
def test_branch_capacity_invalid_zero_and_negative():
    # check invalid capacity branch
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(20, 0, 2)
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(20, -10, 2)

def test_branch_capacity_valid():
    # check valid capacity branch
    assert waitlist_position(20, 50, 0) == 0

def test_branch_seat_available():
    # check enrolled < capacity branch
    assert waitlist_position(49, 50, 0) == 0

def test_branch_course_full_enrolled_equals_or_exceeds_capacity():
    # check enrolled >= capacity branch
    assert waitlist_position(50, 50, 0) == 1
    assert waitlist_position(55, 50, 0) == 1

def test_branch_waitlist_full_boundary_and_over():
    # check waitlist >= 10 full branch
    assert waitlist_position(50, 50, 10) == -1
    assert waitlist_position(50, 50, 12) == -1

def test_branch_waitlist_increment_below_ten():
    # check waitlist < 10 increment branch
    assert waitlist_position(50, 50, 0) == 1
    assert waitlist_position(50, 50, 5) == 6
    assert waitlist_position(50, 50, 9) == 10


# late_fee branch coverage
def test_branch_days_late_zero_and_negative():
    # check on time or early branch
    assert late_fee(0, 15, False) == 0
    assert late_fee(-5, 15, False) == 0

def test_branch_days_late_positive():
    # check positive days late branch
    assert late_fee(1, 15, False) == 500

def test_branch_has_waiver_true():
    # check fee waiver branch
    assert late_fee(5, 15, True) == 0
    assert late_fee(15, 25, True) == 0

def test_branch_has_waiver_false():
    # check no waiver branch
    assert late_fee(5, 15, False) == 500

def test_branch_within_seven_days():
    # check days_late <= 7 branch
    assert late_fee(3, 16, False) == 500
    assert late_fee(7, 16, False) == 500

def test_branch_over_seven_days():
    # check days_late > 7 branch
    assert late_fee(8, 16, False) == 600

def test_branch_credits_boundary_and_over():
    # check credits <= 20 vs credits > 20 branch
    assert late_fee(5, 20, False) == 500
    assert late_fee(5, 21, False) == 750
    assert late_fee(8, 22, False) == 850

def test_branch_fee_cap_and_boundaries():
    # check fee > 2000 cap branch and fee <= 2000 branch
    assert late_fee(25, 15, False) == 2000
    assert late_fee(22, 22, False) == 2000
    assert late_fee(22, 15, False) == 2000
    assert late_fee(10, 15, False) == 800
