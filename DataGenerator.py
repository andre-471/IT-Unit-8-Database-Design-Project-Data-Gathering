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


    # @staticmethod
    # def _index_data(data):       
    #     for i, row in enumerate(data, start=1):
    #         yield [i] + row  # Prepend the row number to each row

    @staticmethod
    def _read_csv(filename):
        with open(os.path.join('data', filename + ".csv"), 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader) # skip first line
            for row in reader:
                yield row

    def generate_departments(self):
        yield dedent("""\
            CREATE TABLE departments (
                dept_id INT NOT NULL AUTO_INCREMENT,
                dept_name VARCHAR(255) NOT NULL,
                PRIMARY KEY (dept_id),
                UNIQUE KEY dept_name (dept_name)
            );""") # idk if you need to repeat dept_name for UNIQUE KEY
        
        for row in DataGenerator._read_csv("departments"):
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
                    REFERENCES departments (dept_id)
                    ON DELETE CASCADE
            );""")

        id = 1

        for row in DataGenerator._read_csv("teachers"):
            yield dedent("""\
                INSERT INTO teachers
                VALUES ({}, '{}', {});""").format(*row)
