import random
from collections import defaultdict

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

        self.teachers: list[int] = []
        self.students: list[int] = []
        self.rooms: list[int] = []
        self.courses: list[int] = []
        self.course_offerings: list[int] = []
        self.course_offerings_per_period: dict[int, list[int]] = defaultdict(list)
        self.students_per_course_offering: dict[int, list[int]] = defaultdict(list)
        self.assignments_per_course_offering: dict[int, list[int]] = defaultdict(list)

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

    # DONE
    def generate_departments(self):
        yield dedent("""\
            CREATE TABLE departments (
                dept_id INT NOT NULL AUTO_INCREMENT,
                dept_name VARCHAR(255) NOT NULL,
                PRIMARY KEY (dept_id),
                UNIQUE KEY (dept_name)
            );""")

        for row in DataGenerator.__read_csv("departments"):
            dept_id, dept_name = row
            dept_id = int(dept_id)

            yield dedent(f"""\
                INSERT INTO departments
                VALUES ({dept_id}, '{dept_name}');""")

    # DONE
    def generate_teachers(self):
        yield dedent("""\
            CREATE TABLE teachers (
                teacher_id INT NOT NULL AUTO_INCREMENT,
                teacher_name VARCHAR(255) NOT NULL,
                dept_id INT NOT NULL,
                PRIMARY KEY (teacher_id),
                UNIQUE KEY (teacher_name),
                FOREIGN KEY (dept_id) 
                    REFERENCES departments (dept_id)
                    ON DELETE CASCADE
            );""")

        for row in DataGenerator.__read_csv("teachers"):
            teacher_id, teacher_name, dept_id = row
            teacher_id, dept_id = int(teacher_id), int(dept_id)

            self.teachers.append(teacher_id)

            yield dedent(f"""\
                INSERT INTO teachers
                VALUES ({teacher_id}, '{teacher_name}', {dept_id});""")


    # DONE
    def generate_rooms(self):
        yield dedent("""\
            CREATE TABLE rooms (
                room_id INT NOT NULL AUTO_INCREMENT,
                room VARCHAR(255) NOT NULL,
                PRIMARY KEY (room_id),
                UNIQUE KEY(room)
            );""")

        room_id = 1
        for floor in ["B", "1", "2", "3", "4", "5", "6", "7", "8"]:
            for wing in ["N", "E", "S", "W"]:
                for number in range(1, 21):
                    room = f"{floor}{wing}{number:02d}"

                    self.rooms.append(room_id)

                    yield dedent(f"""\
                        INSERT INTO rooms
                        VALUES ({room_id}, '{room}');""")
                    room_id += 1

    # DONE
    def generate_students(self):
        yield dedent("""\
            CREATE TABLE students (
                student_id INT NOT NULL AUTO_INCREMENT,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                PRIMARY KEY (student_id)
                """)

        for student_id in range(1, 5001):
            self.students.append(student_id)

            yield dedent(f"""\
                INSERT INTO students
                VALUES ({student_id}, '{self.faker.first_name()}', '{self.faker.last_name()}');""")

    def generate_course_types(self):
        yield dedent("""\
            CREATE TABLE course_types (
                crs_type_id INT NOT NULL,
                crs_type VARCHAR(255) NOT NULL,
                PRIMARY KEY (crs_type_id),
                UNIQUE KEY (crs_type)
            );""")

        for row in DataGenerator.__read_csv("course_types"):
            crs_type_id, crs_type = row
            crs_type_id = int(crs_type_id)

            yield dedent(f"""\
                INSERT INTO course_types
                VALUES ({crs_type_id}, '{type}');""")

    def generate_courses(self):
        yield dedent("""\
            CREATE TABLE courses (
                crs_id INT NOT NULL,
                crs_name VARCHAR(255) NOT NULL,
                crs_type_id INT NOT NULL,
                PRIMARY KEY (crs_id),
                UNIQUE KEY (crs_name),
                FOREIGN KEY (crs_type_id)
                    REFERENCES course_type (crs_type_id)
                    ON DELETE CASCADE
            );""")

        for row in DataGenerator.__read_csv("courses"):
            crs_id, crs_type_id, crs_name = row
            crs_id, crs_type_id = int(crs_id), int(crs_type_id)

            self.courses.append(crs_id)

            yield dedent(f"""\
                       INSERT INTO courses
                       VALUES ({crs_id}, '{crs_name}', {crs_type_id});""")

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
                    ON DELETE CASCADE,
                FOREIGN KEY (room_id)
                    REFERENCES rooms (room_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (teacher_id)
                    REFERENCES teachers (teacher_id)
                    ON DELETE CASCADE
            );""")

        rooms_per_period = {}
        teachers_per_period = {}
        for period in range(1, 11):
            # shuffle the rooms and teachers for each period with the random library
            rooms_per_period[period] = random.sample(self.rooms, len(self.rooms))
            teachers_per_period[period] = random.sample(self.teachers, len(self.teachers))

        offering_id = 1
        for crs_id in self.courses:
            for i in range(random.randint(1, 5)):
                period = random.randint(1, 10)
                room_id = rooms_per_period[period].pop()
                teacher_id = teachers_per_period[period].pop()

                self.course_offerings.append(offering_id)
                self.course_offerings_per_period[period].append(offering_id)

                yield dedent(f"""\
                    INSERT INTO course_offerings
                    VALUES ({offering_id}, {crs_id}, {room_id}, {period}, {teacher_id});""")

                offering_id += 1


    def generate_roster(self):
        yield dedent("""\
            CREATE TABLE roster (
                student_id INT NOT NULL,
                offering_id INT NOT NULL,
                PRIMARY KEY (studednt_id, offering_id),
                FOREIGN KEY (student_id)
                    REFERENCES students (student_id)
                    ON DELETE CASCADE,
                FOREIGN KEY (offering_id)
                    REFERENCES course_offerings (offering_id)
                    ON DELETE CASCADE
            );""")

        for student_id in self.students:
            for period in range(1, 11):
                offering_id = random.choice(self.course_offerings_per_period[period])
                self.students_per_course_offering[offering_id].append(student_id)

                yield dedent(f"""\
                    INSERT INTO roster
                    VALUES ({student_id}, {offering_id});""")


    def generate_assignment_types(self):
        yield dedent("""\
            CREATE TABLE assignment_type (
                asg_type_id INT NOT NULL AUTO_INCREMENT,
                type VARCHAR(255) NOT NULL,
                PRIMARY KEY (asg_type_id)
            );""")
        for row in DataGenerator.__read_csv("assignment_types"):
            asg_type_id, asg_type = row
            asg_type_id = int(asg_type_id)
            # self.assignment_types.append(asg_type_id)  do we need this? no

            yield dedent(f"""\
                INSERT INTO assignment_type
                VALUES ({asg_type_id}, '{asg_type}';""")


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

        asg_id = 1
        for offering_id in self.course_offerings:
            for _ in range(3):
                asg_name = self.faker.catch_phrase()
                asg_type_id = 1  # major assignment

                self.assignments_per_course_offering[offering_id].append(asg_id)

                yield dedent(f"""\
                    INSERT INTO assignments
                    VALUES ({asg_id}, '{asg_name}', {asg_type_id}, {offering_id});""")
                asg_id += 1

            for _ in range(12):
                asg_name = self.faker.catch_phrase()
                asg_type_id = 2  # minor assignment

                self.assignments_per_course_offering[offering_id].append(asg_id)

                yield dedent(f"""\
                    INSERT INTO assignments
                    VALUES ({asg_id}, '{asg_name}', {asg_type_id}, {offering_id});""")
                asg_id += 1

    def generate_grades(self):
        yield dedent("""\
            CREATE TABLE grades (
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

        for offering_id in self.course_offerings:
            asg_ids = self.assignments_per_course_offering[offering_id]
            student_ids = self.students_per_course_offering[offering_id]

            for student_id in student_ids:
                for asg_id in asg_ids:
                    grade: float = round(random.uniform(75, 100), 2)

                    yield dedent(f"""\
                        INSERT INTO grades
                        VALUES ({student_id}, {asg_id}, {grade})""")