import argparse

def get_lab_number():
    parser = argparse.ArgumentParser(description="Grader for 126 lab")
    parser.add_argument('lab', help='the number of the lab', type=int)
    args = parser.parse_args()
    return args.lab
