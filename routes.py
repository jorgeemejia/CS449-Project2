from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List, Union

import contextlib
import sqlite3

from fastapi import Depends, HTTPException, APIRouter, Response, status
from typing import List
from schemas import Student, Class, Department, Instructor, Enrollment   # Import your schemas

router = APIRouter()
instructors_db = []
classes_db = []
students_db = []
enroll_db = []

database = "database.db"

def get_db():
    with contextlib.closing(sqlite3.connect(database, check_same_thread=False)) as db:
        db.row_factory = sqlite3.Row
        yield db

#==========================================students==================================================
  
#creates a student   
def create_student(student_data: Student, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM student WHERE id = ?", (student_data.id,))
    existing_student = cursor.fetchone()
    
    if existing_student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student with this ID already exists")

    cursor.execute("INSERT INTO student (id, name) VALUES (?, ?)", (student_data.id, student_data.name))
    db.commit()
    cursor.close()

    return student_data

#gets available classes for any student
#USES DB
@router.get("/student/classes", response_model=List[Class], tags=['Student']) 
def get_available_classes(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    # Execute the SQL query to retrieve available classes
    cursor.execute("""
        SELECT class.id, class.name, class.course_code, class.section_number, class.current_enroll, class.max_enroll,
               department.id AS department_id, department.name AS department_name,
               instructor.id AS instructor_id, instructor.name AS instructor_name
        FROM class
        INNER JOIN department ON class.department_id = department.id
        INNER JOIN instructor ON class.instructor_id = instructor.id
        WHERE class.current_enroll < class.max_enroll
    """)
    
    # Fetch all rows from the query result
    rows = cursor.fetchall()

    # Convert database rows into Class objects
    available_classes = []
    for row in rows:
        class_data = dict(row)
        class_instance = Class(**class_data)  # Assuming Class has attributes corresponding to database columns
        available_classes.append(class_instance)

    return available_classes



@router.post("/student/{id}/enroll", response_model=Union[Class, Dict[str, str]], tags=['Student'])
def enroll_student_in_class(id: int, class_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    # Check if the student exists in the database
    cursor.execute("SELECT * FROM student WHERE id = ?", (id,))
    student_data = cursor.fetchone()

    # Check if the class exists in the database
    cursor.execute("SELECT * FROM class WHERE id = ?", (class_id,))
    class_data = cursor.fetchone()

    if not student_data or not class_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student or Class not found")

    # Check if the class is full, add student to waitlist if so
    if class_data['current_enroll'] >= class_data['max_enroll']:
        placement = len(enroll_db) + 1
        waitlist_entry = Enrollment(class_id=class_id, student_id=id, placement=placement)
        enroll_db.append(waitlist_entry)
        return {"message": "Student added to the waitlist"}

    # Check if student is already enrolled in the class
    cursor.execute("SELECT * FROM enrollment WHERE class_id = ? AND student_id = ?", (class_id, id))
    existing_enrollment = cursor.fetchone()

    if existing_enrollment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student is already enrolled in this class")
    
    # Increment enrollment number in the database
    new_enrollment = class_data['current_enroll'] + 1
    cursor.execute("UPDATE class SET current_enroll = ? WHERE id = ?", (new_enrollment, class_id))

    # Add student to enrolled class in the database
    placement = None  # Set the placement to None for enrolled students
    cursor.execute("INSERT INTO enrollment (placement, class_id, student_id) VALUES (?, ?, ?)", (placement, class_id, id))
    db.commit()

    # Fetch the updated class data from the database
    cursor.execute("SELECT * FROM class WHERE id = ?", (class_id,))
    updated_class_data = cursor.fetchone()

    # Create a Class object from the updated class data
    enrolled_class = Class(**updated_class_data)

    return enrolled_class




@router.put("/student/{id}/drop/{class_id}", response_model=Class, tags=['Student'])
def drop_student_from_class(id: int, class_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    # check if exist
    cursor.execute("SELECT * FROM student WHERE id = ?", (id,))
    student_data = cursor.fetchone()


    cursor.execute("SELECT * FROM class WHERE id = ?", (class_id,))
    class_data = cursor.fetchone()

    if not student_data or not class_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student or Class not found")

    #check enrollment
    cursor.execute("SELECT * FROM enrollment WHERE student_id = ? AND class_id = ?", (id, class_id))
    enrollment_data = cursor.fetchone()

    if not enrollment_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student is not enrolled in the class")

    # decremenet enrollment
    new_enrollment = class_data['current_enroll'] - 1
    cursor.execute("UPDATE class SET current_enroll = ? WHERE id = ?", (new_enrollment, class_id))

    # remove student from class
    cursor.execute("DELETE FROM enrollment WHERE student_id = ? AND class_id = ?", (id, class_id))
    db.commit()

    # fetch from db
    cursor.execute("SELECT * FROM class WHERE id = ?", (class_id,))
    updated_class_data = cursor.fetchone()

    # create class obj
    updated_class = Class(**updated_class_data)

    return updated_class


#==========================================wait list========================================== 

@router.get("/student/{student_id}/waitlist", response_model=List[Enrollment], tags=['Waitlist'])
def view_waiting_list(student_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    # Retrieve waitlist entries for the specified student from the database
    cursor.execute("SELECT * FROM waitlist WHERE student_id = ?", (student_id,))
    waitlist_data = cursor.fetchall()

    # Convert database rows into Enrollment objects
    student_waitlist = []
    for entry in waitlist_data:
        waitlist_instance = Enrollment(**entry)  # Assuming Enrollment has attributes corresponding to database columns
        student_waitlist.append(waitlist_instance)

    return student_waitlist


@router.put("/student/{student_id}/remove-from-waitlist/{class_id}", tags=['Waitlist'])
def remove_from_waitlist(student_id: int, class_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM waitlist WHERE student_id = ? AND class_id = ?", (student_id, class_id))
    waitlist_entry = cursor.fetchone()

    if waitlist_entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student is not on the waiting list for this class")

    cursor.execute("DELETE FROM waitlist WHERE student_id = ? AND class_id = ?", (student_id, class_id))
    db.commit()

    return {"message": "Student removed from the waiting list"}


#==========================================classes==================================================

#view current enrollment for class
@router.get("/instructor/{instructor_id}/enrollment", response_model=List[Class], tags=['Instructor'])
def get_instructor_enrollment(instructor_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM instructor WHERE id = ?", (instructor_id,))
    instructor_data = cursor.fetchone()

    if not instructor_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")

    cursor.execute("SELECT * FROM class WHERE instructor_id = ?", (instructor_id,))
    enrolled_classes_data = cursor.fetchall()

    enrolled_classes = []
    for class_data in enrolled_classes_data:
        enrolled_class_instance = Class(**class_data)  
        enrolled_classes.append(enrolled_class_instance)

    return enrolled_classes

#view students who have dropped the class
@router.get("/instructor/{instructor_id}/dropped", response_model=List[Class], tags=['Instructor'])
def get_instructor_dropped(instructor_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM instructor WHERE id = ?", (instructor_id,))
    instructor_data = cursor.fetchone()

    if not instructor_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")

    cursor.execute("SELECT * FROM class WHERE instructor_id = ? AND current_enroll < max_enroll", (instructor_id,))
    dropped_classes_data = cursor.fetchall()

    dropped_classes = []
    for class_data in dropped_classes_data:
        dropped_class_instance = Class(**class_data)  
        dropped_classes.append(dropped_class_instance)

    return dropped_classes

#drop students
@router.post("/instructor/{instructor_id}/drop", response_model=Class, tags=['Instructor'])
def instructor_drop_class(instructor_id: int, class_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM instructor WHERE id = ?", (instructor_id,))
    instructor_data = cursor.fetchone()

    if not instructor_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")

    cursor.execute("SELECT * FROM class WHERE id = ? AND instructor_id = ?", (class_id, instructor_id))
    target_class_data = cursor.fetchone()

    if not target_class_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found or instructor is not teaching this class")

    target_class = Class(**target_class_data)  

    return target_class


#==========================================registrar==================================================

#USES DB
@router.post("/registrar/classes/", response_model=Class, tags=['Registrar'])
def create_class(class_data: Class, db: sqlite3.Connection = Depends(get_db)):
    try:
        db.execute(
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
        db.commit()
        return class_data
    except sqlite3.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"type": type(e).__name__, "msg": str(e)}
        )

@router.delete("/registrar/classes/{class_id}", tags=['Registrar'])
def remove_class(class_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    # Check if the class exists in the database
    cursor.execute("SELECT * FROM class WHERE id = ?", (class_id,))
    target_class_data = cursor.fetchone()

    if not target_class_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")

    # Delete the class from the database
    cursor.execute("DELETE FROM class WHERE id = ?", (class_id,))
    db.commit()

    return {"message": "Class removed successfully"}


@router.put("/registrar/classes/{class_id}/instructor/{instructor_id}", tags=['Registrar'])
def change_instructor(class_id: int, instructor_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM class WHERE id = ?", (class_id,))
    target_class_data = cursor.fetchone()

    if not target_class_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")

    cursor.execute("SELECT * FROM instructor WHERE id = ?", (instructor_id,))
    instructor_data = cursor.fetchone()

    if not instructor_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")

    cursor.execute("UPDATE class SET instructor_id = ? WHERE id = ?", (instructor_id, class_id))
    db.commit()

    return {"message": "Instructor changed successfully"}


@router.put("/registrar/automatic-enrollment/freeze", tags=['Registrar'])
def freeze_automatic_enrollment():
    # TDOO implement this
    return {"message": "Automatic enrollment frozen successfully"}
