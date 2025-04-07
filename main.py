import os

from dotenv import find_dotenv, load_dotenv

from datagenerator import DataGenerator
from dbconnection import DBConnection


def check_queries(seed=None):
    if not find_dotenv():
        raise FileNotFoundError(".env file doesn't exist")

    dg = DataGenerator(seed)
    output_dir = 'output'
    sql_runner = 'run_sql.sh'

    load_dotenv()
    user = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    name = os.environ.get('DB_NAME')

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    sql_files = [
        ('clear_output.sql', dg.clear_data()),
        ('departments_output.sql', dg.generate_departments()),
        ('teachers_output.sql', dg.generate_teachers()),
        ('rooms_output.sql', dg.generate_rooms()),
        ('students_output.sql', dg.generate_students()),
        ('course_types_output.sql', dg.generate_course_types()),
        ('courses_output.sql', dg.generate_courses()),
        ('offerings_output.sql', dg.generate_offerings()),
        ('roster_output.sql', dg.generate_roster()),
        ('assignment_types_output.sql', dg.generate_assignment_types()),
        ('assignments_output.sql', dg.generate_assignments()),
        ('grades_output.sql', dg.generate_grades())
    ]

    with open(sql_runner, 'w') as s:
        for filename, queries in sql_files:
            with open(os.path.join(output_dir, filename), 'w') as f:
                for query in queries:
                    f.write(query + '\n')
            s.write(f"mysql -u {user} -p {password} -h 10.8.37.226 -D {name} < output/{filename}")



def execute_all_queries(seed=None):
    # this is more inefficient than just generating the sql file and running it on the server itself
    # 20 min vs 1 hr
    db = DBConnection()
    dg = DataGenerator(seed)

    # db.execute_many(dg.clear_data())
    db.execute_many(dg.generate_departments())
    db.execute_many(dg.generate_teachers())
    db.execute_many(dg.generate_rooms())
    db.execute_many(dg.generate_students())
    db.execute_many(dg.generate_course_types())
    db.execute_many(dg.generate_courses())
    db.execute_many(dg.generate_offerings())
    db.execute_many(dg.generate_roster())
    db.execute_many(dg.generate_assignment_types())
    db.execute_many(dg.generate_assignments())
    db.execute_many(dg.generate_grades())


def main():
    check_queries("hi")
    # execute_all_queries("hi")


if __name__ == "__main__":
    main()
