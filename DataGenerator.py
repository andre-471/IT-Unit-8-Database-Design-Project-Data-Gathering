class DataGenerator:
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

    @staticmethod
    def _index_data(data):       
        for i, row in enumerate(data, start=1):
            yield [i] + row  # Prepend the row number to each row

    @staticmethod
    def departments():
        yield ("""CREATE TABLE departments (
               )""")
        
        #CREATE TABLE departments (dept_id INTEGER PRIMARY KEY, deot_name VARCHAR(255))
