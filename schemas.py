from pydantic import BaseModel

class ClassBase(BaseModel):
    department: str
    course_code: str
    section_number: str
    name: str
    instructor: str
    max_enrollment: int

class ClassCreate(ClassBase):
    pass

class Class(ClassBase):
    id: int
    current_enrollment: int

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    name: str
    student_id: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True

class RegistrarBase(BaseModel):
    name: str
    registar_id: str

class RegistrarCreate(RegistrarBase):
    pass

class Registrar(RegistrarBase):
    id: int

    class Config:
        orm_mode = True
