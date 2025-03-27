import random
from bs4 import BeautifulSoup
from faker import Faker
from textwrap import dedent

import os
import csv
import requests


# for reference: https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
class DataGenerator:
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

    def generate_departments(self):
        yield dedent("""\
            CREATE TABLE departments (
                dept_id INT NOT NULL AUTO_INCREMENT,
                dept_name VARCHAR(255) NOT NULL,
                PRIMARY KEY (dept_id),
                UNIQUE KEY dept_name (dept_name)
            );""")  # idk if you need to repeat dept_name for UNIQUE KEY

        for row in DataGenerator._read_csv("departments"):
            dept_id, dept_name = row
            dept_id = int(dept_id)

            self.departments[dept_id] = dept_name

            yield dedent(f"""\
                INSERT INTO departments
                VALUES ({dept_id}, '{dept_name}');""")

    def generate_teachers(self):
        yield dedent("""\
            CREATE TABLE teachers (
                teacher_id INT NOT NULL AUTO_INCREMENT,
                teacher_name VARCHAR(255) NOT NULL,
                dept_id INT NOT NULL,
                PRIMARY KEY (teacher_id),
                UNIQUE KEY teacher_name (teacher_name),
                FOREIGN KEY (dept_id) 
                    REFERENCES departments (dept_id)
                    ON DELETE CASCADE
            );""")

        for row in DataGenerator._read_csv("teachers"):
            teacher_id, teacher_name, dept_id = row
            teacher_id, dept_id = int(teacher_id), int(dept_id)

            self.teachers[teacher_id] = (teacher_name, dept_id)

            yield dedent(f"""\
                INSERT INTO teachers
                VALUES ({teacher_id}, '{teacher_name}', {dept_id});""")

        print(self.teachers)

    def generate_students(self):
        for i in range(1, 5001):
            yield dedent("""\
                INSERT INTO students
                VALUES ({}, '{}', '{}');""").format(i, self.faker.first_name(), faker.last_name())

    def generate_course_offerings(self):
        yield dedent("""\
            CREATE TABLE course_offerings (
                offering_id INT NOT NULL AUTO_INCREMENT,
                crs_id INT NOT NULL,
                room_id INT NOT NULL,
                period INT NOT NULL,
                teacher_id INT NOT NULL,
                PRIMARY KEY (offering_id),
                FOREIGN KEY (crs_id)
                    REFERENCES courses (crs_id)
                    ON DELETE CASCADE
                FOREIGN KEY (room_id)
                    REFERENCES rooms (room_id)
                    ON DELETE CASCADE
                UNIQUE KEY period (period) -- Is room really that unique if it can repeat
                FOREIGN KEY (teacher_id)
                    REFERENCES teachers (teacher_id)
                    ON DELETE CASCADE
            );""")

        id = 1
        for row in DataGenerator._read_csv("courses"):
            yield dedent("""\
                INSERT INTO courses
                VALUES ({}, {}, {}, {}, {});""").format(*row)
