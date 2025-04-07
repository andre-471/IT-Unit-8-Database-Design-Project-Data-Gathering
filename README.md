# Unit 8 Database Design Project Data Gathering _and Populating_ (GAP)

## Usage:
1. Create `.env` file in root directory with the following information:
    ```text
    DB_USERNAME=[YOUR MYSQL USERNAME]
    DB_PASSWORD=[YOUR MYSQL PASSWORD]
    DB_NAME=[THE MYSQL DATABASE TO POPULATE]
    LINUX_USERNAME=[YOUR LINUX USERNAME]
    LINUX_PASSWORD=[YOUR LINUX PASSWORD]
    ```
    to allow the script to populate the database.
2. Run `main.py`.

### also this code is very inefficient and it _ONLY RUNS ON THE SCHOOL NETWORK_ (unless the mysql server host is changed)

## Roadmap:
course_type and courses should be easy to populate (similar to the teachers one), but maybe use a CSV file instead of a dictionary (convert csv -> data structures)
room is also easy


for offerings:
- create a data structure that is for every period, there is a set of rooms
- create a DS that is for every period, there is a set of teacher ids
- loop through every course and repeat it xRandom times
- for every loop, select a random period and remove a random room and teacher from each set for each period

for rosters:
- create dict with every period = set of offerings
- loop through every student
- select each period random offering (do not remove from set)
- then we good fr fr

for assignment:
- ez lol just for every offering create an assignment

for grades:
- for every student_id in roster, get offering_id
- query assignments for asg_id for each offering_id
- loop through each asg_id and add it for student

use seed to guarantee the same values for every generation of data
