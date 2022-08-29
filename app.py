# app.py
import json
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response, HTMLResponse
from fastapi import FastAPI, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from bson import json_util
from pydantic import EmailStr


from database import db
from auth import get_password_hash


def parse_json(data):
    return json.loads(json_util.dumps(data))


templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_description="Base Route", response_class=HTMLResponse)
async def home(request: Request):
    result = {
        "Message": "Welcome To College Bazaar",
    }
    return templates.TemplateResponse("base.html", {"request": request, "result": result})

#########################################
#  CRUD Operations in MongoDB for Students Collection    #
#########################################

# add new student
'''
    http://127.0.0.1:8000/student/signup
'''


@app.get("/student/signup", response_description="Add new student", response_class=HTMLResponse)
async def create_student(request: Request):
    return templates.TemplateResponse("student_signup.html", {"request": request, "result": None})

'''
    http://127.0.0.1:8000/db/students/add
'''


@app.post("/db/students/add", response_description="Add new student", response_class=HTMLResponse)
async def create_student(request: Request, name: str = Form(...), email: EmailStr = Form(...), password: str = Form(...)):
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
            'hashed_password': hashed_password
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


@app.get("/get/student/{email}", response_description="Get a single student", response_class=HTMLResponse)
async def show_student(request: Request, email: EmailStr):
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
    return templates.TemplateResponse("student_update.html", {"request": request, "result": None})

'''
    http://127.0.0.1:8000/db/students/update
'''


@app.post("/db/students/update", response_description="Update a student", response_class=HTMLResponse)
async def update_student(request: Request, name: str = Form(...), email: EmailStr = Form(...), password: str = Form(...)):
    try:
        if email == None:
            raise HTTPException(status_code=404, detail=f"Student not found")

        student = await db["students"].find_one({"email": email})
        if name == None:
            name = student['name']
        if password == None:
            hashed_password = student['hashed_password']
        else:
            hashed_password = get_password_hash(password)
        updated_student = {
            "$set": {
                'name': name,
                'email': email,
                'password': hashed_password
            }
        }
        filt = {"_id": student['_id']}
        await db["students"].update_one(filt, updated_student)
        result = {
            # 'id': created_student['_id'],
            'name': updated_student["$set"]['name'],
            'email': updated_student["$set"]['email'],
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
async def delete_student(email: EmailStr):
    delete_result = await db["students"].delete_one({"email": email})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student not found")

#########################################
#  CRUD Operations in MongoDB for Admin Collection         #
#########################################

# add new admin
'''
    http://127.0.0.1:8000/admin/signup
'''


@app.get("/admin/signup", response_description="Add new admin", response_class=HTMLResponse)
async def create_admin(request: Request):
    return templates.TemplateResponse("admin_signup.html", {"request": request, "result": None})

'''
    http://127.0.0.1:8000/db/admins/add
'''


@app.post("/db/admins/add", response_description="Add new admin", response_class=HTMLResponse)
async def create_admin(request: Request, name: str = Form(...), email: EmailStr = Form(...), password: str = Form(...)):
    # r_json = await request.json()
    try:
        admin = await db["admins"].find_one({"email": email})
        if admin:
            raise HTTPException(
                status_code=404, detail=f"Email Already Exists")
        hashed_password = get_password_hash(password)
        admin = {
            'name': name,
            'email': email,
            'hashed_password': hashed_password
        }
        new_admin = await db["admins"].insert_one(admin)
        created_admin = await db["admins"].find_one({"_id": new_admin.inserted_id})
        result = {
            # 'id': created_admin['_id'],
            'name': created_admin['name'],
            'email': created_admin['email'],
            'message': "admin created successfully"
        }
        return templates.TemplateResponse("base.html", {"request": request, "result": result})

    except Exception as e:
        return templates.TemplateResponse("base.html", {"request": request, "result": e})

# Get all admins
'''
    http://127.0.0.1:8000/get/admins/all
'''


@app.get("/get/admins/all", response_description="List all admins",  response_class=HTMLResponse)
async def list_admins(request: Request):
    admins = await db["admins"].find().to_list(1000)
    result = {
        'admins ': admins,
        'message': "List of all admins get successfully"
    }
    return templates.TemplateResponse("base.html", {"request": request, "result": result})

# Get one admin
'''
    http://127.0.0.1:8000/get/admin/{email}
'''


@app.get("/get/admin/{email}", response_description="Get a single admin", response_class=HTMLResponse)
async def show_admin(request: Request, email: EmailStr):
    if (admin := await db["admins"].find_one({"email": email})) is not None:
        result = {
            # 'id': created_admin['_id'],
            'name': admin['name'],
            'email': admin['email'],
            'message': "admin info obtained successfully"
        }
        return templates.TemplateResponse("base.html", {"request": request, "result": result})

    raise HTTPException(status_code=404, detail=f"admin not found")

# Update admin
'''
    http://127.0.0.1:8000/update/admin
'''


@app.get("/update/admin", response_description="Update a admin", response_class=HTMLResponse)
async def update_admin(request: Request):
    return templates.TemplateResponse("admin_update.html", {"request": request, "result": None})

'''
    http://127.0.0.1:8000/db/admins/update
'''


@app.post("/db/admins/update", response_description="Update a admin", response_class=HTMLResponse)
async def update_admin(request: Request, name: str = Form(...), email: EmailStr = Form(...), password: str = Form(...)):
    try:
        if email == None:
            raise HTTPException(status_code=404, detail=f"admin not found")

        admin = await db["admins"].find_one({"email": email})
        if name == None:
            name = admin['name']
        if password == None:
            hashed_password = admin['hashed_password']
        else:
            hashed_password = get_password_hash(password)
        updated_admin = {
            "$set": {
                'name': name,
                'email': email,
                'password': hashed_password
            }
        }
        filt = {"_id": admin['_id']}
        await db["admins"].update_one(filt, updated_admin)
        result = {
            # 'id': created_admin['_id'],
            'name': updated_admin["$set"]['name'],
            'email': updated_admin["$set"]['email'],
            'message': "admin updated successfully"
        }
        return templates.TemplateResponse("base.html", {"request": request, "result": result})

    except Exception as e:
        return templates.TemplateResponse("base.html", {"request": request, "result": e})

# Delete admin
'''
    http://127.0.0.1:8000/delete/admin/{email}
'''


@app.delete("/delete/admin/{email}", response_description="Delete a admin")
async def delete_admin(email: EmailStr):
    delete_result = await db["admins"].delete_one({"email": email})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"admin not found")

###########################################
#CRUD Operations in MongoDB for product_post Collection   #
###########################################

# add new product_post
'''
    http://127.0.0.1:8000/product-post/new
'''


@app.get("/product-post/new", response_description="Add new product_post", response_class=HTMLResponse)
async def create_product_post(request: Request):
    return templates.TemplateResponse("product_post_create.html", {"request": request, "result": None})

'''
    http://127.0.0.1:8000/db/product-posts/add
'''


@app.post("/db/product-posts/add", response_description="Add new product-post", response_class=HTMLResponse)
async def create_product_post(request: Request, name: str = Form(...), seller_email: EmailStr = Form(...), description: str = Form(...), price: float = Form(...), image_url: str = Form(...), category: str = Form(...), tags: list = Form(...)):
    # r_json = await request.json()
    try:
        product_post = await db["product_posts"].find_one({"seller_email": seller_email, "name": name})
        if product_post:
            raise HTTPException(
                status_code=404, detail=f"Product Already Posted")

        product_post = {
            'name': name,
            'seller_email': seller_email,
            'description': description,
            'price': price,
            'image_url': image_url,
            'category': category,
            'tags': tags
        }
        new_product_post = await db["product_posts"].insert_one(product_post)
        created_product_post = await db["product_posts"].find_one({"_id": new_product_post.inserted_id})
        result = {
            # 'id': created_product_post['_id'],
            'name': created_product_post['name'],
            'seller_email': created_product_post['seller_email'],
            'description': created_product_post['description'],
            'price': created_product_post['price'],
            'category': created_product_post['category'],
            'tags': created_product_post['tags'],
            'message': "product_post created successfully"
        }
        return templates.TemplateResponse("base.html", {"request": request, "result": result})

    except Exception as e:
        return templates.TemplateResponse("base.html", {"request": request, "result": e})

# Get all product_posts
'''
    http://127.0.0.1:8000/get/product-posts/all
'''


@app.get("/get/product-posts/all", response_description="List all product_posts",  response_class=HTMLResponse)
async def list_product_posts(request: Request):
    product_posts = await db["product_posts"].find().to_list(1000)
    result = {
        'product_posts ': product_posts,
        'message': "List of all product_posts get successfully"
    }
    return templates.TemplateResponse("base.html", {"request": request, "result": result})

# Get one product_post
'''
    http://127.0.0.1:8000/get/product-post/{email}
'''


@app.get("/get/product-post/{seller_email}", response_description="Get all product_post of a student", response_class=HTMLResponse)
async def show_product_post_by_student(request: Request, seller_email: EmailStr):
    if (product_posts := await db["product_posts"].find_one({"seller_email": seller_email})) is not None:
        product_post_list = []
        for product_post in product_posts:
            product_post_data = {
                # 'id': product_post['_id'],
                'name': product_post['name'],
                'seller_email': product_post['seller_email'],
                'description': product_post['description'],
                'price': product_post['price'],
                'image_url': product_post['image_url'],
                'category': product_post['category'],
                'tags': product_post['tags'],
                'message': "product_post created successfully"
            }
            product_post_list.append(product_post_data)
            result = {
                'product_posts': product_post_list,
                'message': "product_post obtained successfully"
            }
            return templates.TemplateResponse("base.html", {"request": request, "result": result})

    raise HTTPException(status_code=404, detail=f"product_post not found")

# Update product_post
'''
    http://127.0.0.1:8000/update/product-post
'''


@app.get("/update/product-post", response_description="Update a product_post", response_class=HTMLResponse)
async def update_product_post(request: Request):
    return templates.TemplateResponse("product_post_update.html", {"request": request, "result": None})

'''
    http://127.0.0.1:8000/db/product-posts/update
'''


@app.post("/db/product-post/update", response_description="Update a product_post", response_class=HTMLResponse)
async def update_product_post(request: Request, name: str = Form(...), seller_email: EmailStr = Form(...), description: str = Form(...), price: float = Form(...), image_url: str = Form(...), category: str = Form(...), tags: list = Form(...)):
    try:
        if seller_email == None or name == None:
            raise HTTPException(
                status_code=404, detail=f"product_post not found")

        product_post = await db["product_posts"].find_one({"seller_email": seller_email, "name": name})
        if description == None:
            description = product_post['description']
        if price == None:
            price = product_post['price']
        if image_url == None:
            image_url = product_post['image_url']
        if category == None:
            category = product_post['category']
        if tags == None:
            tags = product_post['tags']

        updated_product_post = {
            "$set": {
                'name': name,
                'seller_email': seller_email,
                'description': description,
                'price': price,
                'image_url': image_url,
                'category': category,
                'tags': tags
            }
        }
        filt = {"_id": product_post['_id']}
        await db["product_posts"].update_one(filt, updated_product_post)
        result = {
            # 'id': created_product_post['_id'],
            'name': updated_product_post["$set"]['name'],
            'seller_email': updated_product_post["$set"]['seller_email'],
            'description': updated_product_post["$set"]['description'],
            'price': updated_product_post["$set"]['price'],
            'category': updated_product_post["$set"]['category'],
            'tags': updated_product_post["$set"]['tags'],
            'message': "product_post updated successfully"
        }
        return templates.TemplateResponse("base.html", {"request": request, "result": result})

    except Exception as e:
        return templates.TemplateResponse("base.html", {"request": request, "result": e})

# Delete product_post
'''
    http://127.0.0.1:8000/delete/product_post/{email}
'''


@app.delete("/delete/product_post/{seller_email}/{name}", response_description="Delete a product_post")
async def delete_product_post(seller_email: EmailStr, name: str):
    delete_result = await db["product_posts"].delete_one({"seller_email": seller_email, "name": name})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"product_post not found")
