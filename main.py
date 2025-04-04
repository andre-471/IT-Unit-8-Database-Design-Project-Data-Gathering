import os

from datagenerator import DataGenerator
from dbconnection import DBConnection


def check_queries(seed=None):
    dg = DataGenerator(seed)

    output_dir = 'output'
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    with open(os.path.join(output_dir, 'clear_output.sql'), 'w') as f:
        for query in dg.clear_data():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'departments_output.sql'), 'w') as f:
        for query in dg.generate_departments():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'teachers_output.sql'), 'w') as f:
        for query in dg.generate_teachers():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'rooms_output.sql'), 'w') as f:
        for query in dg.generate_rooms():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'students_output.sql'), 'w') as f:
        for query in dg.generate_students():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'course_types_output.sql'), 'w') as f:
        for query in dg.generate_course_types():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'courses_output.sql'), 'w') as f:
        for query in dg.generate_courses():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'offerings_output.sql'), 'w') as f:
        for query in dg.generate_offerings():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'roster_output.sql'), 'w') as f:
        for query in dg.generate_roster():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'assignment_types_output.sql'), 'w') as f:
        for query in dg.generate_assignment_types():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'assignments_output.sql'), 'w') as f:
        for query in dg.generate_assignments():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'grades_output.sql'), 'w') as f:
        for query in dg.generate_grades():
            f.write(query + '\n')


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
