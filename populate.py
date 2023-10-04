import sqlite3
import os
from schemas import Class, Student, Department, Instructor, Enrollment

#Remove database if it exists before creating and populating it
if os.path.exists("database.db"):
    os.remove("database.db")

sample_departments = [
    Department(id=1, name="CHEM"),
    Department(id=2, name="CPSC"),
    Department(id=3, name="ENGL"),
    Department(id=4, name="MATH"),
    Department(id=5, name="PHYS"),
]

sample_instructors = [
    Instructor(id=1, name="Kennyt Avery"),
    Instructor(id=2, name="John Smith"),
    Instructor(id=3, name="Jane Doe"),
    Instructor(id=4, name="Mike Hawk"),
]

sample_students = [
    Student(id=1, name="Homer Simpson"),
    Student(id=2, name="Philly J. Fry"),
    Student(id=3, name="Angel Santoyo"),
    Student(id=4, name="David Carlson"),
    Student(id=5, name="Steve Smith"),
    Student(id=6, name="Bob Taylor"),
    Student(id=7, name="Joe Schmoe"),
    Student(id=8, name="Michael Carey"),
]

sample_classes = [
    Class(
        id=1,
        name="Web Back-End Engineering",
        course_code="449",
        section_number="01",
        current_enroll=0,
        max_enroll=30,
        department_id=2,
        instructor_id=1,
    ),
    Class(
        id=2,
        name="Web Front-End Engineering",
        course_code="349",
        section_number="02",
        current_enroll=0,
        max_enroll=30,
        department_id=2,
        instructor_id=1,
    ),
    Class(
        id=3,
        name="Introduction to Computer Science",
        course_code="120",
        section_number="08",
        current_enroll=0,
        max_enroll=30,
        department_id=2,
        instructor_id=2,
    ),
    Class(
        id=4,
        name="Calculus I",
        course_code="150",
        section_number="04",
        current_enroll=0,
        max_enroll=30,
        department_id=4,
        instructor_id=3,
    ),
    Class(
        id=5,
        name="Calculus I",
        course_code="101",
        section_number="10",
        current_enroll=30,
        max_enroll=30,
        department_id=3,
        instructor_id=4,
    ),
]

sample_enrollments = [
    Enrollment(
        placement=2,
        class_id=5,
        student_id=1,
    ),
    Enrollment(
        placement=1,
        class_id=5,
        student_id=2,
    ),
    Enrollment(
        placement=31,
        class_id=5,
        student_id=4,
    ),
]

""" create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print("Error:", e)

    return conn

""" create a table from the create_table_sql statement
:param conn: Connection object
:param create_table_sql: a CREATE TABLE statement
:return:
"""
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print("Error:", e)

def select_query(conn, query):
    try:
        c = conn.cursor()
        c.execute(query)
        rows = c.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print("Error:", e)

# populates db
def populate_database():
    database = "database.db"
    conn = create_connection(database)
    
    department_table = """ CREATE TABLE IF NOT EXISTS department ( 
                            id integer NOT NULL PRIMARY KEY UNIQUE,
                            name text NOT NULL
                        ); """
    create_table(conn, department_table)
    
    instructor_table = """ CREATE TABLE IF NOT EXISTS instructor ( 
                            id integer NOT NULL PRIMARY KEY UNIQUE,
                            name text NOT NULL
                        ); """
    create_table(conn, instructor_table)
    
    student_table = """ CREATE TABLE IF NOT EXISTS student ( 
                            id integer NOT NULL PRIMARY KEY UNIQUE,
                            name text NOT NULL
                        ); """
    create_table(conn, student_table)
    
    class_table = """ CREATE TABLE IF NOT EXISTS class (
                        id integer NOT NULL PRIMARY KEY UNIQUE,
                        name text NOT NULL,
                        course_code text NOT NULL,
                        section_number text NOT NULL,
                        current_enroll integer,
                        max_enroll integer,
                        department_id integer,
                        instructor_id integer,
                        FOREIGN KEY(department_id) REFERENCES department(id),
                        FOREIGN KEY(instructor_id) REFERENCES instructor(id)
                    ); """
    create_table(conn, class_table)
    
    enrollment_table = """ CREATE TABLE IF NOT EXISTS enrollment (
                            placement integer NOT NULL,
                            class_id integer,
                            student_id integer,
                            FOREIGN KEY(class_id) REFERENCES class(id),
                            FOREIGN KEY(student_id) REFERENCES student(id)
                    ); """
    create_table(conn, enrollment_table)

    cursor = conn.cursor()
    for department_data in sample_departments:
        cursor.execute(
            """
            INSERT INTO department (id, name)
            VALUES (?, ?)
            """,
            (department_data.id, department_data.name)
        )

    for instructor_data in sample_instructors:
        cursor.execute(
            """
            INSERT INTO instructor (id, name)
            VALUES (?, ?)
            """,
            (instructor_data.id, instructor_data.name)
        )
    
    for student_data in sample_students:
        cursor.execute(
            """
            INSERT INTO student (id, name)
            VALUES (?, ?)
            """,
            (student_data.id, student_data.name)
        )
    
    for class_data in sample_classes:
        cursor.execute(
            """
            INSERT INTO class (id, name, course_code, section_number, current_enroll, max_enroll, department_id, instructor_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                class_data.id,
                class_data.name,
                class_data.course_code,
                class_data.section_number,
                class_data.current_enroll,
                class_data.max_enroll,
                class_data.department_id,
                class_data.instructor_id
            )
        )

    for enrollment_data in sample_enrollments:
        cursor.execute(
            """
            INSERT INTO enrollment (placement, class_id, student_id)
            VALUES (?, ?, ?)
            """,
            (
            enrollment_data.placement, 
            enrollment_data.class_id,
            enrollment_data.student_id
            )
        )

    conn.commit()
    cursor.close()
    print("--- test to see if population worked ---")
    
    query = "SELECT * FROM department"
    print(query)
    select_query(conn, query)
    
    query = "SELECT * FROM instructor"
    print(query)
    select_query(conn, query)
    
    query = "SELECT * FROM student"
    print(query)
    select_query(conn, query)
    
    query = "SELECT * FROM class"
    print(query)
    select_query(conn, query)
    
    query = "SELECT * FROM enrollment"
    print(query)
    select_query(conn, query)

    conn.close()

    print("Database populated :D")

if __name__ == "__main__":
    populate_database()