from textwrap import dedent


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
    for row in self._read_csv("courses"):
        yield dedent("""\
            INSERT INTO courses
            VALUES ({}, {}, {}, {}, {});""").format(*row)