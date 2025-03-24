import os
import csv
import requests
from faker import Faker
from bs4 import BeautifulSoup

def check_data_dir():
    if not os.path.isdir('data'):
        os.mkdir('data')

def write_to_data_dir(filename, header, data):
    with open(os.path.join('data', filename + ".csv"), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

def enumerate_data(data):
    for i, row in enumerate(data, start=1):
        yield [i] + row  # Prepend the row number to each row

def generate_rooms():
    header = ["room_id", "room"]
    data = []

    for floor in ["B", "1", "2", "3", "4", "5", "6", "7", "8"]:
        for wing in ["N", "E", "S", "W"]:
            for room in range(1, 21):
                room_number = f"{floor}{wing}{room:02d}"
                data.append([room_number])

    write_to_data_dir("rooms", header, enumerate_data(data))

def generate_teachers():
    header = ["teacher_id", "teacher"]
    data = []

    request = requests.get("https://www.bths.edu/apps/staff/")
    beautiful_soup = BeautifulSoup(request.content, "html.parser")
    staff_category = beautiful_soup.find(id="staff").find_all(class_="staff-categoryStaffMember")
    for a in staff_category:
        print(a.dl.dt.get_text(strip=True), a.dl.dd.get_text(strip=True)) # doesn't fully work yet

def main():
    # check_data_dir()

    # generate_teachers()

    # generate_rooms()

    # fake = Faker()
    # print(fake.name())
    
    

if __name__ == "__main__":
    main()