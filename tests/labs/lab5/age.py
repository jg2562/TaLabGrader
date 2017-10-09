import sys
import random
import string
import grader.utils

function_str_name = "Update and Get age"

def generate_random_string(length):
    return ''.join([random.choice(string.ascii_lowercase) for i in range(length)])

def generate_number():
    phone = "{:03d}-{:03d}-{:04d}".format(random.randint(0,999), random.randint(0,999), random.randint(0,9999))
    return phone

def generate_email():
    return generate_random_string(8) + "@gmail.com"

def generate_age():
    return random.randint(10,60)

def generate_fake_person():
    first = generate_random_string(7)
    last = generate_random_string(10)
    email = generate_email()
    phone = generate_number()
    age = generate_age()
    return (first, last, email, age, phone)

def check_function_exists(studentCode):
    try:
        studentCode.update_contact_age()
    except AttributeError:
        return (False, "Failed to find function called 'update_contact_number'")
    except TypeError:
        pass

    try:
        studentCode.get_contact_age()
    except AttributeError:
        return (False, "Failed to find function called 'get_contact_number'")
    except TypeError:
        pass
    return (True, "All functions detected")


def check_age_function(studentCode):
    try:
        people_amount = 100
        fake_people = [ generate_fake_person() for i in range(people_amount)]
        contacts = {}
        add_people = set()
        for person in fake_people[:people_amount//2]:
            studentCode.create_contact(contacts, person[0], person[1], person[2], person[3], person[4])
            add_people.add(person)

        random.shuffle(fake_people)

        for person in fake_people:
            new_num = generate_age()
            studentCode.update_contact_age(contacts, person[0], person[1], new_num)
            if studentCode.get_contact_age(contacts, person[0], person[1]) != new_num:
                return (False, "{} doesn't work".format(function_str_name))
        return (True, "{} number functions work".format(function_str_name))

    except Exception as e:
        return (False, "{} throw an exception".format(function_str_name))

def get_test_functions():
    return [(check_function_exists, 0.25, "Checking {} function exists".format(function_str_name)),
            (check_age_function, 0.75, "Veriying {} functions".format(function_str_name))]

# Need to check if both the same first name or last name won't be a problem
