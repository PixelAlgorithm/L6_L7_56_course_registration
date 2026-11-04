# Prajwal M - PES2UG24CS910
# Lab 6: Course Registration Tests

import pytest
from course_registration import can_register, waitlist_position, late_fee
from BranchCoverageTest_course_registration import *

# starter test cases
def test_registered():
    assert can_register("regular", 20, 4, True) == "registered"

def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0
