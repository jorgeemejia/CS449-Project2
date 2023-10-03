from pydantic import BaseModel
from typing import List

class Department(BaseModel):
    id: int
    name: str

class Instructor(BaseModel):
    id: int
    name: str

class Class(BaseModel):
    id: int
    name: str
    course_code: str
    section_number: str
    current_enroll: int
    max_enroll: int
    #Decided to get fancy and use nested models,
    #unsure if this is useful or not
    department: Department | None = None
    instructor: Instructor | None = None


class Student(BaseModel):
    id: int
    name: str
    enrolled_classes: List[Class] = [] 

class Waitlist(BaseModel):
    class_id: int
    student_id: int
    placement: int

