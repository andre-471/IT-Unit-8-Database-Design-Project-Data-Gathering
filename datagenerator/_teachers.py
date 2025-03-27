from textwrap import dedent

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

    for row in self._read_csv("teachers"):
        teacher_id, teacher_name, dept_id = row
        teacher_id, dept_id = int(teacher_id), int(dept_id)

        self.teachers[teacher_id] = (teacher_name, dept_id)

        yield dedent(f"""\
            INSERT INTO teachers
            VALUES ({teacher_id}, '{teacher_name}', {dept_id});""")

    print(self.teachers)


def generate_departments(self):
    yield dedent("""\
        CREATE TABLE departments (
            dept_id INT NOT NULL AUTO_INCREMENT,
            dept_name VARCHAR(255) NOT NULL,
            PRIMARY KEY (dept_id),
            UNIQUE KEY dept_name (dept_name)
        );""")  # idk if you need to repeat dept_name for UNIQUE KEY

    for row in self._read_csv("departments"):
        dept_id, dept_name = row
        dept_id = int(dept_id)

        self.departments[dept_id] = dept_name

        yield dedent(f"""\
            INSERT INTO departments
            VALUES ({dept_id}, '{dept_name}');""")