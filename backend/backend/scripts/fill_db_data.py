import os.path
import sqlite3
import psycopg2
from typing import Union
import faker
import random
from backend.config import DEBUG, LOCAL_DB
from backend.database import get_connection

# Initialize Faker instance
fake = faker.Faker()

# Grade thresholds
GRADE_THRESHOLDS = [
    ('A+', 90, 100),
    ('A', 80, 90),
    ('B', 70, 80),
    ('C', 60, 70),
    ('D', 50, 60),
    ('F', 0, 50)
]

def create_tables(connection: Union[sqlite3.Connection, psycopg2.extensions.connection]):
    cursor = connection.cursor()

    create_students_table = """
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        date_of_birth DATE NOT NULL,
        stream TEXT DEFAULT NULL,
        current_class_id INTEGER NOT NULL REFERENCES classes(class_id)
    )
    """
    create_classes_table = """
    CREATE TABLE IF NOT EXISTS classes (
        class_id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_name TEXT NOT NULL
    )
    """
    create_subjects_table = """
    CREATE TABLE IF NOT EXISTS subjects (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_name TEXT NOT NULL UNIQUE
    )
    """
    create_grades_table = """
    CREATE TABLE IF NOT EXISTS grades (
        grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
        grade TEXT NOT NULL UNIQUE,
        min_percentage REAL NOT NULL,
        max_percentage REAL NOT NULL
    )
    """
    create_marks_table = """
    CREATE TABLE IF NOT EXISTS marks (
        mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL REFERENCES students(student_id),
        subject_id INTEGER NOT NULL REFERENCES subjects(subject_id),
        class_id INTEGER NOT NULL REFERENCES classes(class_id),
        marks INTEGER NOT NULL
    )
    """
    create_classes_subjects_table = """
    CREATE TABLE IF NOT EXISTS class_subjects (
        class_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        PRIMARY KEY (class_id, subject_id),
        FOREIGN KEY (class_id) REFERENCES classes(class_id),
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    )
    """

    cursor.execute(create_classes_table)
    cursor.execute(create_subjects_table)
    cursor.execute(create_grades_table)
    cursor.execute(create_students_table)
    cursor.execute(create_marks_table)
    cursor.execute(create_classes_subjects_table)
    connection.commit()

    # Insert grade thresholds into grades table
    if isinstance(connection, psycopg2.extensions.connection):
        cursor.executemany(
            "INSERT INTO grades (grade, min_percentage, max_percentage) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
            GRADE_THRESHOLDS
        )
    elif isinstance(connection, sqlite3.Connection):
        cursor.executemany(
            "INSERT INTO grades (grade, min_percentage, max_percentage) VALUES (?, ?, ?) ON CONFLICT DO NOTHING;",
            GRADE_THRESHOLDS
        )
    connection.commit()

def insert_fake_data(connection: Union[sqlite3.Connection, psycopg2.extensions.connection]):
    cursor = connection.cursor()

    # Insert classes for grades 5th to 10th
    classes_5_to_10 = [
        "5th Grade", "6th Grade", "7th Grade", "8th Grade", "9th Grade", "10th Grade"
    ]

    # Insert subjects for grades 5th to 10th
    subjects_5_to_10 = [
        "Mathematics", "Science", "Social Science", "English", "Hindi", "Retail", "Information Technology"
    ]

    # Insert classes and get their IDs
    class_ids_5_to_10 = {}
    for class_name in classes_5_to_10:
        if isinstance(connection, psycopg2.extensions.connection):
            cmd = "INSERT INTO classes (class_name) VALUES (%s) RETURNING class_id;"
        elif isinstance(connection, sqlite3.Connection):
            cmd = "INSERT INTO classes (class_name) VALUES (?) RETURNING class_id;"

        cursor.execute(cmd, (class_name,))
        class_ids_5_to_10[class_name] = cursor.fetchone()[0]

    connection.commit()

    # Insert subjects and get their IDs, ensuring no duplicates
    subject_ids = {}
    for subject_name in subjects_5_to_10:
        if isinstance(connection, psycopg2.extensions.connection):
            # Check if subject already exists
            cmd_check = "SELECT subject_id FROM subjects WHERE subject_name = %s;"
            cursor.execute(cmd_check, (subject_name,))
            existing_subject = cursor.fetchone()
            if existing_subject:
                subject_id = existing_subject[0]
            else:
                cmd_insert = "INSERT INTO subjects (subject_name) VALUES (%s) RETURNING subject_id;"
                cursor.execute(cmd_insert, (subject_name,))
                subject_id = cursor.fetchone()[0]
        elif isinstance(connection, sqlite3.Connection):
            # Check if subject already exists
            cmd_check = "SELECT subject_id FROM subjects WHERE subject_name = ?;"
            cursor.execute(cmd_check, (subject_name,))
            existing_subject = cursor.fetchone()
            if existing_subject:
                subject_id = existing_subject[0]
            else:
                cmd_insert = "INSERT INTO subjects (subject_name) VALUES (?) RETURNING subject_id;"
                cursor.execute(cmd_insert, (subject_name,))
                subject_id = cursor.fetchone()[0]

        subject_ids[subject_name] = subject_id

    connection.commit()

    # Insert grade thresholds
    for grade, min_perc, max_perc in GRADE_THRESHOLDS:
        if isinstance(connection, psycopg2.extensions.connection):
            cmd = "INSERT INTO grades (grade, min_percentage, max_percentage) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;"
        elif isinstance(connection, sqlite3.Connection):
            cmd = "INSERT INTO grades (grade, min_percentage, max_percentage) VALUES (?, ?, ?) ON CONFLICT DO NOTHING;"
        cursor.execute(cmd, (grade, min_perc, max_perc))

    connection.commit()

    # Generate fake students for classes 5th to 10th
    num_students_5_to_10 = {}
    for class_name in classes_5_to_10:
        num_students_5_to_10[class_name] = random.randint(100, 150)  # Random number of students per class

    for class_name, num_students in num_students_5_to_10.items():
        class_id = class_ids_5_to_10[class_name]
        for _ in range(num_students):
            full_name = fake.name()
            date_of_birth = fake.date_of_birth(minimum_age=10, maximum_age=18)

            # Insert student
            if isinstance(connection, psycopg2.extensions.connection):
                cmd = "INSERT INTO students (full_name, date_of_birth, stream, current_class_id) VALUES (%s, %s, %s, %s) RETURNING student_id;"
            elif isinstance(connection, sqlite3.Connection):
                cmd = "INSERT INTO students (full_name, date_of_birth, stream, current_class_id) VALUES (?, ?, ?, ?) RETURNING student_id;"
            cursor.execute(cmd, (full_name, date_of_birth, None, class_id))
            student_id = cursor.fetchone()[0]

            # Generate marks for each subject
            for subject_name, subject_id in subject_ids.items():
                marks = random.randint(0, 100)

                if isinstance(connection, psycopg2.extensions.connection):
                    cmd = "INSERT INTO marks (student_id, subject_id, class_id, marks) VALUES (%s, %s, %s, %s);"
                elif isinstance(connection, sqlite3.Connection):
                    cmd = "INSERT INTO marks (student_id, subject_id, class_id, marks) VALUES (?, ?, ?, ?);"
                cursor.execute(cmd, (student_id, subject_id, class_id, marks))

    connection.commit()

    # Insert classes for grades 11 and 12
    classes_11_12 = {
        "Science Stream": [
            "Physics", "Chemistry", "Biology", "Mathematics", "Computer Science", "Electronics",
            "Biotechnology", "Psychology", "Engineering Drawing", "Informatics Practices"
        ],
        "Commerce Stream": [
            "Accountancy", "Business Studies", "Economics", "Mathematics", "Informatics Practices",
            "Entrepreneurship", "Statistics", "Business Mathematics"
        ],
        "Humanities/Arts Stream": [
            "History", "Geography", "Political Science", "Sociology", "Psychology", "Philosophy",
            "Economics", "Mathematics", "Fine Arts", "Home Science", "Physical Education",
            "Computer Science", "Informatics Practices"
        ]
    }

    # Insert subjects for grades 11 and 12
    all_subjects = set()
    for subjects_list in classes_11_12.values():
        all_subjects.update(subjects_list)

    # Insert subjects and get their IDs, ensuring no duplicates
    for subject_name in all_subjects:
        if isinstance(connection, psycopg2.extensions.connection):
            # Check if subject already exists
            cmd_check = "SELECT subject_id FROM subjects WHERE subject_name = %s;"
            cursor.execute(cmd_check, (subject_name,))
            existing_subject = cursor.fetchone()
            if existing_subject:
                subject_id = existing_subject[0]
            else:
                cmd_insert = "INSERT INTO subjects (subject_name) VALUES (%s) RETURNING subject_id;"
                cursor.execute(cmd_insert, (subject_name,))
                subject_id = cursor.fetchone()[0]
        elif isinstance(connection, sqlite3.Connection):
            # Check if subject already exists
            cmd_check = "SELECT subject_id FROM subjects WHERE subject_name = ?;"
            cursor.execute(cmd_check, (subject_name,))
            existing_subject = cursor.fetchone()
            if existing_subject:
                subject_id = existing_subject[0]
            else:
                cmd_insert = "INSERT INTO subjects (subject_name) VALUES (?) RETURNING subject_id;"
                cursor.execute(cmd_insert, (subject_name,))
                subject_id = cursor.fetchone()[0]

        subject_ids[subject_name] = subject_id

    connection.commit()

    # Insert classes and get their IDs for grades 11 and 12
    class_ids_11_12 = {}
    for stream in classes_11_12.keys():
        for class_name in ["11th Grade", "12th Grade"]:
            if isinstance(connection, psycopg2.extensions.connection):
                cmd = "INSERT INTO classes (class_name) VALUES (%s) RETURNING class_id;"
            elif isinstance(connection, sqlite3.Connection):
                cmd = "INSERT INTO classes (class_name) VALUES (?) RETURNING class_id;"
            _name = f"{class_name} - {stream}"
            cursor.execute(cmd, (_name,))
            class_id = cursor.fetchone()[0]
            class_ids_11_12[_name] = class_id

    connection.commit()

    # Generate fake students for grades 11 and 12 streams
    num_students_11_12 = {}
    for stream in classes_11_12.keys():
        for class_name in ["11th Grade", "12th Grade"]:
            _name = f"{class_name} - {stream}"
            num_students_11_12[_name] = random.randint(100, 150) # Random number of students per stream

    for stream, num_students in num_students_11_12.items():
        for _ in range(num_students):
            full_name = fake.name()
            class_id = class_ids_11_12[stream]
            date_of_birth = fake.date_of_birth(minimum_age=16, maximum_age=19)

            # Insert student
            if isinstance(connection, psycopg2.extensions.connection):
                cmd = "INSERT INTO students (full_name, date_of_birth, stream, current_class_id) VALUES (%s, %s, %s, %s) RETURNING student_id;"
            elif isinstance(connection, sqlite3.Connection):
                cmd = "INSERT INTO students (full_name, date_of_birth, stream, current_class_id) VALUES (?, ?, ?, ?) RETURNING student_id;"
            cursor.execute(cmd, (full_name, date_of_birth, stream.split("-")[-1].strip(), class_id))
            student_id = cursor.fetchone()[0]

            # Generate marks for each subject in the stream
            for subject_name in classes_11_12[stream.split("-")[-1].strip()]:
                marks = random.randint(0, 100)
                subject_id = subject_ids[subject_name]

                if isinstance(connection, psycopg2.extensions.connection):
                    cmd = "INSERT INTO marks (student_id, subject_id, class_id, marks) VALUES (%s, %s, %s, %s);"
                elif isinstance(connection, sqlite3.Connection):
                    cmd = "INSERT INTO marks (student_id, subject_id, class_id, marks) VALUES (?, ?, ?, ?);"
                cursor.execute(cmd, (student_id, subject_id, class_id, marks))

    connection.commit()

    for class_name in classes_5_to_10:
        for subject_name in subjects_5_to_10:
            if isinstance(connection, psycopg2.extensions.connection):
                subCmd = "INSERT INTO class_subjects (class_id, subject_id) VALUES (%s, %s);"
            elif isinstance(connection, sqlite3.Connection):
                subCmd = "INSERT INTO class_subjects (class_id, subject_id) VALUES (?, ?);"

            cursor.execute(subCmd, (class_ids_5_to_10[class_name], subject_ids[subject_name]))

    connection.commit()

    for stream in classes_11_12.keys():
        for class_name in ["11th Grade", "12th Grade"]:
            for subject_name in classes_11_12[stream]:
                if isinstance(connection, psycopg2.extensions.connection):
                    subCmd = "INSERT INTO class_subjects (class_id, subject_id) VALUES (%s, %s);"
                elif isinstance(connection, sqlite3.Connection):
                    subCmd = "INSERT INTO class_subjects (class_id, subject_id) VALUES (?, ?);"

                class_id = class_ids_11_12[f"{class_name} - {stream}"]
                cursor.execute(subCmd, (class_id, subject_ids[subject_name]))

    connection.commit()


def setup_db():
    connection = get_connection(not DEBUG)

    if DEBUG and os.path.isfile(LOCAL_DB):
        connection.close()
        os.replace(LOCAL_DB, f"{LOCAL_DB}.old")
        connection = get_connection(not DEBUG)

    create_tables(connection)
    insert_fake_data(connection)
    connection.close()

if __name__ == '__main__':
    setup_db()
