# app.py
import json
import os
from unittest import result
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from typing import Optional, List
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from bson import json_util

from models import StudentModel
from database import db
from auth import verify_password, get_password_hash,authenticate_user

def parse_json(data):
    return json.loads(json_util.dumps(data))


templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

#########################################
#  CRUD Operations in MongoDB for Students Collection    #
#########################################

# add new student
'''
    http://127.0.0.1:8000/signup
'''


@app.get("/signup", response_description="Add new student", response_class=HTMLResponse)
async def create_student(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "result": None})

'''
    http://127.0.0.1:8000/db/students/add
'''


@app.post("/db/students/add", response_description="Add new student", response_class=HTMLResponse)
async def create_student(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # r_json = await request.json()
    try:
        student = await db["students"].find_one({"email": email})
        if student:
            raise HTTPException(
                status_code=404, detail=f"Email Already Exists")
        hashed_password = get_password_hash(password)
        student = {
            'name': name,
            'email': email,
            'hashed_password': password
        }
        new_student = await db["students"].insert_one(student)
        created_student = await db["students"].find_one({"_id": new_student.inserted_id})
        result = {
            # 'id': created_student['_id'],
            'name': created_student['name'],
            'email': created_student['email'],
            'message': "Student created successfully"
        }
        return templates.TemplateResponse("base.html", {"request": request, "result": result})

    except Exception as e:
        return templates.TemplateResponse("base.html", {"request": request, "result": e})

# Get all students
'''
    http://127.0.0.1:8000/get/students/all
'''


@app.get("/get/students/all", response_description="List all students",  response_class=HTMLResponse)
async def list_students(request: Request):
    students = await db["students"].find().to_list(1000)
    result = {
        'students ': students,
        'message': "List of all students get successfully"
    }
    return templates.TemplateResponse("base.html", {"request": request, "result": result})

# Get one Student
'''
    http://127.0.0.1:8000/get/student/{email}
'''


@app.get("/get/student/{email}", response_description="Get a single student",response_class=HTMLResponse)
async def show_student(request: Request, email: str):
    if (student := await db["students"].find_one({"email": email})) is not None:
        result = {
            # 'id': created_student['_id'],
            'name': student['name'],
            'email': student['email'],
            'message': "Student info obtained successfully"
        }
        return templates.TemplateResponse("base.html", {"request": request, "result": result})

    raise HTTPException(status_code=404, detail=f"Student not found")

# Update Student
'''
    http://127.0.0.1:8000/update/student
'''


@app.get("/update/student", response_description="Update a student", response_class=HTMLResponse)
async def update_student(request: Request):
    return templates.TemplateResponse("update.html", {"request": request, "result": None})

'''
    http://127.0.0.1:8000/db/students/update
'''


@app.post("/db/students/update", response_description="Update a student", response_class=HTMLResponse)
async def update_student(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        if email == None:
            raise HTTPException(status_code=404, detail=f"Student not found")

        student = await db["students"].find_one({"email": email})
        updated_student = {
            "$set": {
                'name': name,
                'email': email,
                'password': password
            }
        }
        filt = {"_id": student['_id']}
        await db["students"].update_one(filt, updated_student)
        result = {
            # 'id': created_student['_id'],
            'name': updated_student['name'],
            'email': updated_student['email'],
            'message': "Student updated successfully"
        }
        return templates.TemplateResponse("base.html", {"request": request, "result": result})

    except Exception as e:
        return templates.TemplateResponse("base.html", {"request": request, "result": e})

# Delete Student
'''
    http://127.0.0.1:8000/delete/student/{email}
'''

@app.delete("/delete/student/{email}", response_description="Delete a student")
async def delete_student(email: str):
    delete_result = await db["students"].delete_one({"email": email})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student not found")

