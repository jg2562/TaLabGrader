import sys
import random
import string
import grader.utils

function_str_name = "Update and Get age"

def get_letter_dict():
    pass

def get_test_functions():
    return [(check_function_exists, 0.25, "Checking {} function exists".format(function_str_name)),
            (check_age_function, 0.75, "Veriying {} functions".format(function_str_name))]

# Need to check if both the same first name or last name won't be a problem
