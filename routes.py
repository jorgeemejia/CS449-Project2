from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from fastapi import Depends, HTTPException, APIRouter
from typing import List
from schemas import Student, Class, Registrar  # Import your schemas

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

class Registrar(BaseModel):
    name: str
    registar_id: str

classes_db = []
students_db = []
registrar_db = []

@router.post("/classes/", response_model=Student)
def create_class(class_data: Class):
    # Check if a class with the same course_code and section_number already exists
    for existing_class in classes_db:
        if existing_class.course_code == class_data.course_code and existing_class.section_number == class_data.section_number:
            raise HTTPException(status_code=400, detail="Class with this code and section already exists")

    classes_db.append(class_data)
    return class_data

@router.get("/classes/", response_model=List[Class])
def list_classes():
    return classes_db



@router.post("/students/", response_model=Student)
def create_student(student_data: Student):
    # Check if a student with the same student_id already exists
    for existing_student in students_db:
        if existing_student.student_id == student_data.student_id:
            raise HTTPException(status_code=400, detail="Student with this ID already exists")

    students_db.append(student_data)
    return student_data

@router.get("/students/", response_model=List[Student])
def list_students():
    return students_db

@router.post("/registrar/", response_model=Registrar)
def create_registrar(registrar_data: Registrar):
    # Check if a registrar with the same student_id already exists
    for existing_registrar in registrar_db:
        if existing_registrar.registar_id == registrar_data.registar_id:
            raise HTTPException(status_code=400, detail="Registrar with this ID already exists")

    registrar_db.append(registrar_data)
    return registrar_data

@router.get("/registrar/", response_model=List[Registrar])
def list_registrars():
    return registrar_db


