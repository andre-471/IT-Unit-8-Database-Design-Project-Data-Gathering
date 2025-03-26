import random
from bs4 import BeautifulSoup
from faker import Faker
from textwrap import dedent

import requests

# for reference: https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html
class DataGenerator:
    def __init__(self, seed=None):
        random.seed(seed)
        Faker.seed(seed)

        self.departments = [
            [1, 'Biology'],
            [2, 'Chemistry'],
            [3, 'Physics'],
            [4, 'CS & Engineering'],
            [5, 'English'],
            [6, 'Health & PE'],
            [7, 'Mathematics'],
            [8, 'Social Studies'],
            [9, 'Special Education'],
            [10, 'Visual & Performing Arts'],
            [11, 'World Languages & ENL']
        ]

        self.departments_staff_list = {
            1: 30105,
            2: 30106,
            3: 18378,
            4: 18376,
            5: 18377,
            6: 18381,
            7: 18380,
            8: 18383,
            9: 95973,
            10: 314031,
            11: 18379,
        }

    # @staticmethod
    # def _index_data(data):       
    #     for i, row in enumerate(data, start=1):
    #         yield [i] + row  # Prepend the row number to each row

    def generate_departments(self):
        yield dedent("""\
            CREATE TABLE departments (
                dept_id INT NOT NULL AUTO_INCREMENT,
                dept_name VARCHAR(255) NOT NULL,
                PRIMARY KEY (dept_id),
                UNIQUE KEY dept_name (dept_name)
            );""") # idk if you need to repeat dept_name for UNIQUE KEY
        
        for row in self.departments:
            yield dedent("""\
                INSERT INTO departments
                VALUES ({}, '{}');""").format(*row)
            

    def generate_teachers(self):
        yield dedent("""\
            CREATE TABLE teachers (
                teacher_id INT NOT NULL AUTO_INCREMENT,
                teacher_name VARCHAR(255) NOT NULL,
                dept_id INT NOT NULL,
                PRIMARY KEY (teacher_id),
                UNIQUE KEY teacher_name (teacher_name),
                FOREIGN KEY (dept_id) 
                    REFERENCES departments(dept_id)
                    ON DELETE CASCADE
            );""")

        id = 1

        for department_id in self.departments_staff_list:
            request = requests.get(f"https://www.bths.edu/apps/pages/index.jsp?uREC_ID={self.departments_staff_list[department_id]}&type=d&termREC_ID=&pREC_ID=staff")
            beautiful_soup = BeautifulSoup(request.content, "html.parser")
            staff_category = beautiful_soup.find(id="staff").find_all(class_="staff-categoryStaffMember")
            for element in staff_category:
                teacher = element.dl.dt.get_text(strip=True)
                if ". " in teacher: # for Mr. or Ms. or Mrs. etc...
                    teacher = teacher.split(". ")[1:] # TODO: fix so that it doesn't break if there are more than one dot

                yield dedent("""\
                    INSERT INTO teachers
                    VALUES ({}, '{}', {});""").format(id, teacher, department_id)
                id += 1
