#routes not asked for but that may be useful for testing,



#delete a student by student id (dropping students from a class may look similar)
@router.delete("/students/{student_id}")
def delete_student(student_id: str):
    # Find the student by student_id
    for student in students_db:
        if student.student_id == student_id:
            students_db.remove(student)
            return {"message": "Student deleted successfully"}

    raise HTTPException(status_code=404, detail="Student not found")

#delete a class
@router.delete("/classes/{course_code}-{section_number}")
def delete_class(course_code: str, section_number: str):
    for class_instance in classes_db:
        if class_instance.course_code == course_code and class_instance.section_number == section_number:
            classes_db.remove(class_instance)
            return {"message": "Class deleted successfully"}

    raise HTTPException(status_code=404, detail="Class not found")

#Wip drop course

# @router.delete("/classes/{student_id}")
# def drop_course(student_id: str):
#     # Find the student by student_id
#     for student in students_db:
#         if student.student_id == student_id:
#             students_db.remove(student)
#             return {"message": "Student deleted successfully"}

#     raise HTTPException(status_code=404, detail="Student not found")