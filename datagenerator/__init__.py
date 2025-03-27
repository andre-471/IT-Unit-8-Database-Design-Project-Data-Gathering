import random
from faker import Faker
from textwrap import dedent

import os
import csv
import requests


# for reference: https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
class DataGenerator:
    from ._teachers import generate_teachers, generate_departments
    from ._students import generate_students, generate_roster
    from ._courses import generate_courses, generate_course_type, generate_course_offerings
    from ._assignments import generate_assignments, generate_assignment_type, generate_grades

    def __init__(self, seed=None):
        random.seed(seed)
        Faker.seed(seed)
        self.faker = Faker()

        self.departments = {}
        self.teachers = {}

    # @staticmethod
    # def _index_data(data):       
    #     for i, row in enumerate(data, start=1):
    #         yield [i] + row  # Prepend the row number to each row

    @staticmethod
    def _read_csv(filename):
        with open(os.path.join('data', filename + ".csv"), 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                yield row
