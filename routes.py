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
@router.post("/students/", response_model=Student, tags=['Student'])
def create_student(student_data: Student):
    for existing_student in students_db:
        if existing_student.id == student_data.id:
            raise HTTPException(status_code=400, detail="Student with this ID already exists")

    students_db.append(student_data)
    return student_data

#gets available classes for any student
#USES DB
@router.get("/student/classes", tags=['Student'])
def get_available_classes(db: sqlite3.Connection = Depends(get_db)):
    query = db.execute("""SELECT class.name, department.name, course_code, section_number, 
                            instructor.name, current_enroll, max_enroll
                            FROM class 
                                INNER JOIN department ON department.id = class.department_id
                                INNER JOIN instructor ON instructor.id = class.instructor_id
                            WHERE current_enroll < max_enroll""")
    rows = query.fetchall()

    # Create a list of dictionaries, where each dictionary represents a row of data
    classes = []
    for row in rows:
        class_name, department_name, course_code, section_number, instructor_name, current_enroll, max_enroll = row
        classes.append({
            "class_name": class_name,
            "department_name": department_name,
            "course_code": course_code,
            "section_number": section_number,
            "instructor_name": instructor_name,
            "current_enroll": current_enroll,
            "max_enroll": max_enroll
        })
    
    return {"Classes": classes}


@router.post("/student/{id}/enroll", response_model=Union[Class, Dict[str, str]], tags=['Student'])  
def enroll_student_in_class(id: int, class_id: int):
    # get student and class
    student = next((std for std in students_db if std.id == id), None)
    target_class = next((cls for cls in classes_db if cls.id == class_id), None)

    # error handle 
    if student is None or target_class is None:
        raise HTTPException(status_code=404, detail="Student or Class not found")

    # check class is full, add student to waitlist if so
    if target_class.current_enroll >= target_class.max_enroll:
        waitlist_entry = Enrollment(class_id=class_id, student_id=id, placement=len(enroll_db) + 1)
        enroll_db.append(waitlist_entry)
        return {"message": "Student added to the waitlist"}

    # increment enrollment number
    target_class.current_enroll += 1

    # add to enrolled class
    student.enrolled_classes.append(target_class)
    return target_class  



@router.put("/student/{id}/drop/{class_id}", response_model=Class, tags=['Student'])
def drop_student_from_class(id: int, class_id: int):
    student = next((std for std in students_db if std.id == id), None)
    target_class = next((cls for cls in classes_db if cls.id == class_id), None)

    if student is None or target_class is None:
        raise HTTPException(status_code=404, detail="Student or Class not found")

    if target_class not in student.enrolled_classes:
        raise HTTPException(status_code=400, detail="Student is not enrolled in the class")

    target_class.current_enroll -= 1

    student.enrolled_classes.remove(target_class)

    return target_class

#==========================================wait list========================================== 

@router.get("/student/{student_id}/waitlist", response_model=List[Enrollment], tags=['Waitlist']) 
def view_waiting_list(student_id: int):
    student_waitlist = [waitlist for waitlist in enroll_db if waitlist.student_id == student_id]
    return student_waitlist

@router.put("/student/{student_id}/remove-from-waitlist/{class_id}", tags=['Waitlist']) 
def remove_from_waitlist(student_id: int, class_id: int):
    # Check if the student is on the waitlist for the specified class
    waitlist_entry = next((entry for entry in enroll_db if entry.student_id == student_id and entry.class_id == class_id), None)
    if waitlist_entry is None:
        raise HTTPException(status_code=404, detail="Student is not on the waiting list for this class")

    enroll_db.remove(waitlist_entry)

    return {"message": "Student removed from the waiting list"}

#==========================================classes==================================================

#view current enrollment for class
@router.get("/instructor/{instructor_id}/enrollment", response_model=List[Class], tags=['Classes']) #works tested
def get_instructor_enrollment(instructor_id: int):
    instructor = next((inst for inst in instructors_db if inst.id == instructor_id), None)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    enrolled_classes = [cls for cls in classes_db if cls.instructor and cls.instructor.id == instructor_id]
    return enrolled_classes

#view students who have dropped the class
@router.get("/instructor/{instructor_id}/dropped", response_model=List[Class], tags=['Classes'])
def get_instructor_dropped(instructor_id: int):
    instructor = next((inst for inst in instructors_db if inst.id == instructor_id), None)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    dropped_classes = [cls for cls in classes_db if cls.instructor and cls.instructor.id == instructor_id and cls.current_enroll < cls.max_enroll]
    return dropped_classes

#drop students
@router.post("/instructor/{instructor_id}/drop", response_model=Class, tags=['Classes'])
def instructor_drop_class(instructor_id: int, class_id: int):
    instructor = next((inst for inst in instructors_db if inst.id == instructor_id), None)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    
    target_class = next((cls for cls in classes_db if cls.id == class_id and cls.instructor and cls.instructor.id == instructor_id), None)
    if not target_class:
        raise HTTPException(status_code=404, detail="Class not found or instructor is not teaching this class")

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
def remove_class(class_id: int):
    target_class = next((cls for cls in classes_db if cls.id == class_id), None)
    if target_class is None:
        raise HTTPException(status_code=404, detail="Class not found")

    classes_db.remove(target_class)
    return {"message": "Class removed successfully"}

@router.put("/registrar/classes/{class_id}/instructor/{instructor_id}", tags=['Registrar']) 
def change_instructor(class_id: int, instructor_id: int):
    target_class = next((cls for cls in classes_db if cls.id == class_id), None)
    if target_class is None:
        raise HTTPException(status_code=404, detail="Class not found")

    target_class.instructor.id = instructor_id
    return {"message": "Instructor changed successfully"}

@router.put("/registrar/automatic-enrollment/freeze", tags=['Registrar'])
def freeze_automatic_enrollment():
    # TDOO implement this
    return {"message": "Automatic enrollment frozen successfully"}


@router.get("/classes/", response_model=List[Class], tags=['Classes'])
def list_classes():
    return classes_db