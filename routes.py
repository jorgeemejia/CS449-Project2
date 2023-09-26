from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Class(BaseModel):
    department: str
    course_code: str
    section_number: str
    name: str
    instructor: str
    current_enrollment: int
    max_enrollment: int

class Student(BaseModel):
    name: str
    student_id: str

classes_db = []
students_db = []

# Define route endpoints and their functions
@router.post("/classes/", response_model=Class)
def create_class(class_data: Class):
    classes_db.append(class_data)
    return class_data

@router.get("/classes/", response_model=List[Class])
def list_classes():
    return classes_db

@router.post("/students/", response_model=Student)
def create_student(student_data: Student):
    students_db.append(student_data)
    return student_data

@router.get("/students/", response_model=List[Student])
def list_students():
    return students_db

