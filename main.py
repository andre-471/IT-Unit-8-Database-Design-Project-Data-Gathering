import os
import csv
import requests
from faker import Faker
from bs4 import BeautifulSoup
from DBConnection import DBConnection
from DataGenerator import DataGenerator

def check_data_dir():
    if not os.path.isdir('data'):
        os.mkdir('data')

def write_to_data_dir(filename, header, data):
    with open(os.path.join('data', filename + ".csv"), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

def index_data(data):
    for i, row in enumerate(data, start=1):
        yield [i] + row  # Prepend the row number to each row

def generate_rooms():
    header = ("room_id", "room")
    data = []

    for floor in ["B", "1", "2", "3", "4", "5", "6", "7", "8"]:
        for wing in ["N", "E", "S", "W"]:
            for room in range(1, 21):
                room_number = f"{floor}{wing}{room:02d}"
                data.append([room_number])

    write_to_data_dir("rooms", header, index_data(data))

def generate_teachers():
    header = ("teacher_id", "teacher", "department")
    data = []

    departments = {
        "Biology": 30105,
        "Chemistry": 30106,
        "Physics": 18378,
        "CTE, Computer Science & Engineering": 18376,
        "English": 18377,
        "Health & PE": 18381,
        "Mathematics": 18380,
        "Social Studies": 18383,
        "Special Education": 95973,
        "Visual & Performing Arts": 314031,
        "World Languages & ENL": 18379,
    }

    for department in departments:
        request = requests.get(f"https://www.bths.edu/apps/pages/index.jsp?uREC_ID={departments[department]}&type=d&termREC_ID=&pREC_ID=staff")
        beautiful_soup = BeautifulSoup(request.content, "html.parser")
        staff_category = beautiful_soup.find(id="staff").find_all(class_="staff-categoryStaffMember")
        for a in staff_category:
            teacher = a.dl.dt.get_text(strip=True)
            if ". " in teacher: # for Mr. or Ms. or Mrs. etc...
                teacher = teacher.split(". ")[1]

            data.append([teacher, department])

    write_to_data_dir("teachers", header, index_data(data))

# WILL BE RANDOM EVERY TIME
def generate_students():
    header = ("student_id", "first_name", "last_name")
    data = []

    faker = Faker()
    Faker.seed("b")

    for i in range(5000):
        data.append([faker.first_name(), faker.last_name()])

    write_to_data_dir("students", header, index_data(data))


def main():
        
    # DBConnection().disconnect()

    # for a in DataGenerator.departments:
    #     print(a)
    
    # check_data_dir()
    # generate_teachers()

    # for query in DataGenerator().generate_teachers():
    #     print(query)
    # generate_students()


    # # generate_teachers()

    # generate_rooms()

    # fake = Faker()
    # print(fake.name())
    
    

if __name__ == "__main__":
    main()