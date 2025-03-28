import random
from faker import Faker
from textwrap import dedent

import os
import csv


# for reference: https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
class DataGenerator:
    def __init__(self, seed=None):
        random.seed(seed)
        Faker.seed(seed)

        self.faker = Faker()

        self.teachers: set[int] = set()
        self.rooms: set[int] = set()

    # @staticmethod
    # def _index_data(data):       
    #     for i, row in enumerate(data, start=1):
    #         yield [i] + row  # Prepend the row number to each row

    @staticmethod
    def __read_csv(filename):
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

        for row in DataGenerator.__read_csv("departments"):
            dept_id, dept_name = row
            dept_id = int(dept_id)

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

        for row in DataGenerator.__read_csv("teachers"):
            teacher_id, teacher_name, dept_id = row
            teacher_id, dept_id = int(teacher_id), int(dept_id)

            self.teachers.add(teacher_id)

            yield dedent(f"""\
                INSERT INTO teachers
                VALUES ({teacher_id}, '{teacher_name}', {dept_id});""")

        print(self.teachers)

    def generate_rooms(self):
        yield dedent("""\
            CREATE TABLE rooms (
                room_id INT NOT NULL AUTO_INCREMENT,
                room VARCHAR(255) NOT NULL,
                PRIMARY KEY (room_id),
                UNIQUE KEY room (room)
            );""")

        room_id = 1
        for floor in ["B", "1", "2", "3", "4", "5", "6", "7", "8"]:
            for wing in ["N", "E", "S", "W"]:
                for number in range(1, 21):
                    room = f"{floor}{wing}{number:02d}"

                    self.rooms.add(room_id)

                    yield dedent(f"""\
                        INSERT INTO rooms
                        VALUES ({room_id}, '{room}');""")
                    room_id += 1

    def generate_students(self):
        yield dedent("""\
            CREATE TABLE students (
                student_id INT NOT NULL AUTO_INCREMENT
                """)

        for i in range(1, 5001):
            yield dedent("""\
                INSERT INTO students
                VALUES ({}, '{}', '{}');""").format(i, self.faker.first_name(), self.faker.last_name())

    def generate_course_type(self):
        yield dedent("""\
            CREATE TABLE course_type )
                     crs_type_id INT NOT NULL,
                     crs_type VARCHAR(255) NOT NULL,
                     PRIMARY KEY (crs_type_id)
            );""")

    def generate_courses(self):
        yield dedent("""\
            CREATE TABLE courses )
                crs_id INT NOT NULL,
                crs_name VARCHAR(255) NOT NULL,
                crs_type_id INT NOT NULL,
                FOREIGN KEY (crs_type_id)
                    REFERENCES course_tyoe (crs_type_id)
                    ON DELETE CASCADE,
                UNIQUE KEY crs_name (crs_name),
                PRIMARY KEY (crs_id)
            );""")

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
        for row in DataGenerator.__read_csv("courses"):
            yield dedent("""\
                INSERT INTO courses
                VALUES ({}, {}, {}, {}, {});""").format(*row)

    def generate_roster(self):
        yield dedent("""\
            CREATE TABLE roster (
                offering_id INT NOT NULL,
                student_id INT NOT NULL,
                FOREIGN KEY (offering_id)
                    REFERENCES COURSES_OFFERINGS (offering_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (student_id)
                    REFERENCE tudents (student_id)
                    ON DELETE CASCADE,
                PRIMARY KEY (offering_id)
            );""")

    def generate_assignment_type(self):
        yield dedent("""\
            CREATE TABLE assignment_type (
                asg_type_id INT NOT NULL,
                type VARCHAR(255) NOT NULL,
                PRIMARY KEY (asg_type_id)
            );""")

    def generate_assignments(self):
        yield dedent("""\
            CREATE TABLE assignments (
                asg_id INT NOT NULL AUTO_INCREMENT,
                asg_name VARCHAR(255) NOT NULL,
                asg_type_id INT NOT NULL,
                offering_id INT NOT NULL,
                FOREIGN KEY (offering_id)
                    REFERENCES course_offerings (offering_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (asg_type_id)
                    REFERENCES assignment_type (asg_type_id)
                    ON DELETE CASCADE,
                PRIMARY KEY (asg_id)
            );""")

    def generate_grades(self):
        yield dedent("""\
            CREATE TABLE assignments (
                student_id NOT NULL,
                asg_id INT NOT NULL,
                grade FLOAT NOT NULL,
                FOREIGN KEY (student_ID)
                     REFERNCES students (student_id)
                     ON DELETE CASCADE,
                FOREIGN KEY (asg_id)
                     REFERENCES assignments (asg_id)
                     ON DELETE CASCADE
            );""")
