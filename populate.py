import sqlite3
from schemas import Class, Student 

sample_classes = [
    Class(
        department="CPSC",
        course_code="449",
        section_number="001",
        name="Web Back-End Engineering",
        instructor="Kennyt Avery",
        current_enrollment=25,
        max_enrollment=30,
    ),
     Class(
        department="CPSC",
        course_code="349",
        section_number="233430",
        name="Web Front-End Engineering",
        instructor="Kennyt Avery",
        current_enrollment=25,
        max_enrollment=30,
    ),    Class(
        department="CPSC",
        course_code="120",
        section_number="1344",
        name="Introduction to Computer Science",
        instructor="Prof. Smith",
        current_enrollment=45,
        max_enrollment=50,
    ),
    Class(
        department="MATH",
        course_code="150",
        section_number="002",
        name="Calculus I",
        instructor="Prof. Johnson",
        current_enrollment=30,
        max_enrollment=40,
    ),
    Class(
        department="ENGL",
        course_code="101",
        section_number="003",
        name="Composition and Rhetoric",
        instructor="Prof. Davis",
        current_enrollment=20,
        max_enrollment=25,
    ),
    Class(
        department="PHYS",
        course_code="210",
        section_number="004",
        name="Physics I",
        instructor="Prof. Adams",
        current_enrollment=28,
        max_enrollment=30,
    ),
    Class(
        department="CHEM",
        course_code="220",
        section_number="005",
        name="Chemistry II",
        instructor="Prof. Miller",
        current_enrollment=22,
        max_enrollment=25,
    ),
]

sample_students = [
    Student(name="homer simpson", student_id="ab34223"),
    Student(name="Philly J. Fry", student_id="D3456"),
    Student(name="Angel Santoyo", student_id="LB23456"),
    Student(name="David Carlson", student_id="A23456"),
    Student(name="John Smith", student_id="J23456"),
    Student(name="Steve Smith", student_id="Pf3456"),
    Student(name="Bob Taylor", student_id="Bf3456"),
    Student(name="Joe Schmoe", student_id="Af3456"),

]

sample_registrar = [
    Registrar(name="John Smith", registar_id ="1")
]

# populates db
def populate_database():
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        for class_data in sample_classes:
            cursor.execute(
                """
                INSERT INTO classes (department, course_code, section_number, name, instructor, current_enrollment, max_enrollment)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    class_data.department,
                    class_data.course_code,
                    class_data.section_number,
                    class_data.name,
                    class_data.instructor,
                    class_data.current_enrollment,
                    class_data.max_enrollment,
                ),
            )

        for student_data in sample_students:
            cursor.execute(
                """
                INSERT INTO students (name, student_id)
                VALUES (?, ?)
                """,
                (student_data.name, student_data.student_id),
            )

        for registrar_data in sample_registrar:
            cursor.execute(
                """
                INSERT INTO students (name, registrar_id)
                VALUES (?, ?)
                """,
                (registrar_data.name, registrar_data.registrar_id),
            )

        conn.commit()
        cursor.close()
        conn.close()

        print("Database populated :D")

    except sqlite3.Error as e:
        print("Error:", e)

if __name__ == "__main__":
    populate_database()
