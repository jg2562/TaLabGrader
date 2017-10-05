import sys
import random
import string
import grader.utils

def generate_random_string(length):
    return ''.join([random.choice(string.ascii_lowercase) for i in range(length)])

def generate_fake_person():
    first = generate_random_string(7)
    last = generate_random_string(10)
    email = generate_random_string(8) + "@gmail.com"
    phone = "{:03d}-{:03d}-{:04d}".format(random.randint(0,999), random.randint(0,999), random.randint(0,9999))
    age = random.randint(10,60)
    return (first, last, email, age, phone)

def check_function_exists(studentCode):
    try:
        studentCode.create_contact()
    except AttributeError:
        return (False, "Failed to find function called 'create_contact'")
    except TypeError:
        pass

    try:
        studentCode.contains_contact()
    except AttributeError:
        return (False, "Failed to find function called 'contains_contact'")
    except TypeError:
        pass
    return (True, "All functions detected")


def check_creation_function(studentCode):
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
            if (studentCode.contains_contact(contacts, person[0], person[1])) != (person in add_people):
                return (False, "Create or contains contact doesn't work")
        return (True, "Create and contains functions work")
    except Exception as e:
        return (False, "Creation or contains throw an exception")


def get_test_functions():
    return [(check_function_exists, 0.25, "Checking create and contains function exists"),
            (check_creation_function, 0.75, "Veriying create and contains functions")]

# Need to check if both the same first name or last name won't be a problem
