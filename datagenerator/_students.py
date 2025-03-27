from textwrap import dedent


def generate_students(self):
    yield dedent("""\
        CREATE TABLE students (
            student_id INT NOT NULL AUTO_INCREMENT
            """)

    for i in range(1, 5001):
        yield dedent("""\
            INSERT INTO students
            VALUES ({}, '{}', '{}');""").format(i, self.faker.first_name(), self.faker.last_name())
        
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