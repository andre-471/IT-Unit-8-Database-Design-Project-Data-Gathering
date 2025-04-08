import os

from dotenv import find_dotenv, load_dotenv

from datagenerator import DataGenerator
from dbconnection import DBConnection

import paramiko, paramiko.util


def run_queries_on_server(seed=None):
    if not find_dotenv():
        raise FileNotFoundError(".env file doesn't exist")

    if not os.path.isdir("logs"):
        os.mkdir("logs")

    paramiko.util.log_to_file("logs/paramiko.log")

    dg = DataGenerator(seed)
    output_dir = "sql_files"
    sql_runner = "run_sql.sh"

    load_dotenv()
    db_user = os.environ.get("DB_USERNAME")
    db_password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")
    linux_user = os.environ.get("LINUX_USERNAME")
    linux_password = os.environ.get("LINUX_PASSWORD")

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    sql_files = [
        ("clear_output.sql", dg.clear_data()),
        ("departments_output.sql", dg.generate_departments()),
        ("teachers_output.sql", dg.generate_teachers()),
        ("rooms_output.sql", dg.generate_rooms()),
        ("students_output.sql", dg.generate_students()),
        ("course_types_output.sql", dg.generate_course_types()),
        ("courses_output.sql", dg.generate_courses()),
        ("offerings_output.sql", dg.generate_offerings()),
        ("roster_output.sql", dg.generate_roster()),
        ("assignment_types_output.sql", dg.generate_assignment_types()),
        ("assignments_output.sql", dg.generate_assignments()),
        ("grades_output.sql", dg.generate_grades())
    ]

    with open(sql_runner, "w", newline="\n") as s:
        s.write("#!/bin/bash\n")

        for filename, queries in sql_files:
            with open(os.path.join(output_dir, filename), "w") as f:
                for query in queries:
                    f.write(query + "\n")
            s.write(f"mysql -u {db_user} -p{db_password} -h 10.8.37.226 -D {db_name} < /home/{linux_user}/Projects/Database_Design_Project/{output_dir}/{filename}\n")

    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("10.8.37.99", username=linux_user, password=linux_password)

        ssh.exec_command(f"rm -f /home/{linux_user}/Projects/Database_Design_Project/{sql_runner}")
        ssh.exec_command(f"rm -f /home/{linux_user}/Projects/Database_Design_Project/{sql_runner}.out")
        ssh.exec_command(f"rm -rf /home/{linux_user}/Projects/Database_Design_Project/{output_dir}/*.sql")  # remove files in output folder

        ssh.exec_command(f"mkdir -p /home/{linux_user}/Projects/Database_Design_Project/{output_dir}")  # also creates Database_Design_Project directory

        with ssh.open_sftp() as sftp:
            sftp.put(sql_runner, f"/home/{linux_user}/Projects/Database_Design_Project/{sql_runner}")

            for filename, _ in sql_files:
                sftp.put(os.path.join(output_dir, filename), f"/home/{linux_user}/Projects/Database_Design_Project/{output_dir}/{filename}")

        ssh.exec_command(f"chmod +x /home/{linux_user}/Projects/Database_Design_Project/{sql_runner}")
        ssh.exec_command(f"nohup /home/{linux_user}/Projects/Database_Design_Project/{sql_runner} &> /home/{linux_user}/Projects/Database_Design_Project/{sql_runner}.log &")

    os.remove(sql_runner)

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
    run_queries_on_server("hi")
    # execute_all_queries("hi")


if __name__ == "__main__":
    main()
