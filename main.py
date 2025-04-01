import os

from dbconnection import DBConnection
from datagenerator import DataGenerator

def check_queries():
    dg = DataGenerator("seed")

    output_dir = 'output'
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    with open(os.path.join(output_dir, 'departments_output.txt'), 'w') as f:
        for query in dg.generate_departments():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'teachers_output.txt'), 'w') as f:
        for query in dg.generate_teachers():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'rooms_output.txt'), 'w') as f:
        for query in dg.generate_rooms():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'students_output.txt'), 'w') as f:
        for query in dg.generate_students():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'course_types_output.txt'), 'w') as f:
        for query in dg.generate_course_types():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'courses_output.txt'), 'w') as f:
        for query in dg.generate_courses():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'course_offerings_output.txt'), 'w') as f:
        for query in dg.generate_course_offerings():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'roster_output.txt'), 'w') as f:
        for query in dg.generate_roster():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'assignment_types_output.txt'), 'w') as f:
        for query in dg.generate_assignment_types():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'assignments_output.txt'), 'w') as f:
        for query in dg.generate_assignments():
            f.write(query + '\n')

    with open(os.path.join(output_dir, 'grades_output.txt'), 'w') as f:
        for query in dg.generate_grades():
            f.write(query + '\n')


def main():
    check_queries()

if __name__ == "__main__":
    main()
