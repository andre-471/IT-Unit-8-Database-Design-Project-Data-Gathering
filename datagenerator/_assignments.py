from textwrap import dedent


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