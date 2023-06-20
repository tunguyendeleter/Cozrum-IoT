from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

class Student(BaseModel):
    name : str
    age : int
    year : str

app = FastAPI()

students = {
    1: {
        "name" : "join",
        "age" : 17,
        "year" : "year 12"
    }
}
@app.get("/")
def index():
    return {"name": "first data"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int):
    return students[student_id]
@app.get("/get-by-name")
def get_student(*,name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data: not found"}
@app.post("/create-student/{student_id}")
def create_student(student_id : int, student : Student):
    if student_id in students:
        return {"Error": "Student exists"}
    students[student_id] = student
    return students[student_id]
