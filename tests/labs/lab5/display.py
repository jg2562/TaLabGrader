import sys
import random
import string
import grader.utils
import io
import contextlib

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
        studentCode.display()
    except AttributeError:
        return (False, "Failed to find function called 'create_contact'")
    except TypeError:
        pass
    return (True, "All functions detected")

def check_display_function(studentCode):
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
            student_out = io.StringIO()
            with contextlib.redirect_stdout(student_out):
                studentCode.display(contacts, person[0], person[1])
            student_out.seek(0)
            student_str = "".join(student_out.readlines())
            person_str = ""
            if person in add_people:
                person_str = "{} {}\nEmail: {}\nPhone: {}\nAge: {}".format(person[0], person[1], person[2], person[4], person[3])
                if person_str.lower().strip() != student_str.lower().strip():
                    return (False, "Display information not correct")
            else:
                if not student_str.strip():
                    return (False, "Display information not correct")

        return (True, "Display information correct")
    except Exception as e:
        print(e)
        return (False, "Display function throw an exception")


def get_test_functions():
    return [(check_function_exists, 0.25, "Checking display exists"),
            (check_display_function, 0.75, "Veriying display function")]
