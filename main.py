from http.client import HTTPException
import sqlite3
import bcrypt
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from requests import request

import sqlite3


conn=sqlite3.connect("Faculty")
cursor=conn.cursor()
try:
    conn.execute('BEGIN')
    cursor.execute("create table Faculty 'Name' varchar(25) 'Department' varchar2(30), 'Fid' int(10), 'Mobile' int(10), 'Email' varchar2(40)")

    conn.commit()
except Exception as e:
    print(e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()   

app=FastAPI()
templates=Jinja2Templates(directory="templates")
@app.get('/Faculty-details',response_class=HTMLResponse)
def Faculty(request:Request):
    conn=sqlite3.connect("Faculty")
    cursor=conn.cursor()
    try:   
        conn.execute('BEGIN')
        cursor.execute("select * from Faculty")
        Faculty_details=cursor.fetchall()
        print(Faculty_details)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
        # Faculty_details=[]
    finally:
        cursor.close()
        conn.close()
    return templates.TemplateResponse("index.html", {"request": request,"data": Faculty_details})

@app.post('/add-faculty')
def add_faculty(Name:str=Form(...),Department:str=Form(...),Fid:str=Form(...),Mobile:str=Form(...),Email:str=Form(...)):
    conn=sqlite3.connect("Faculty")
    cursor=conn.cursor()
    try:
        query=f"insert into Faculty (Name,Department,Fid,Mobile,Email) values('{Name}','{Department}','{Fid}','{Mobile}','{Email}')"
        print(query)
        conn.execute('BEGIN')
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
    return True

@app.post("/delete-faculty")
def delete_faculty(Fid:str=Form(...)):
    conn=sqlite3.connect("Faculty")
    cursor=conn.cursor()
    try:
        query=f"delete from Faculty where (Fid) = ('{Fid}')"
        print(query)
        conn.execute('BEGIN')
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
    return True


@app.get("/departments")
async def get_departments():
    conn = sqlite3.connect("Faculty")
    cursor = conn.cursor()
    try:
        query = "SELECT DISTINCT Department FROM Faculty"
        cursor.execute(query)
        departments = [row[0] for row in cursor.fetchall()]
        return departments
    except Exception as e:
        print("Error fetching departments:", e)
        return []
    finally:
        cursor.close()
        conn.close()

@app.post("/select-department")
async def search_department(request: Request, Department: dict):
  conn=sqlite3.connect("Faculty")
  cursor=conn.cursor()
  selected_department = Department.get('Department')
  try:
    query=f"SELECT *  FROM Faculty where Department=('{selected_department}') "
    print(query)
    conn.execute('BEGIN')
    cursor.execute(query) 
    Faculty=cursor.fetchall()
    print(Faculty)
    conn.commit()
  except Exception as e:
    conn.rollback()
  finally:
    cursor.close()
    conn.close()  
  return Faculty



# Define a function to fetch all faculty members
def fetch_faculty():
    conn = sqlite3.connect("Faculty")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Faculty")
        faculty = cursor.fetchall()
        return faculty
    finally:
        cursor.close()
        conn.close()

# Define a function to delete a faculty member by their Fid
def delete_faculty(fid):
    conn = sqlite3.connect("Faculty")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Faculty WHERE Fid=?", (fid,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# Route to handle GET requests for displaying faculty details
@app.get("/Faculty-details", response_class=HTMLResponse)
async def display_faculty(request: Request):
    faculty = fetch_faculty()
    return templates.TemplateResponse("index.html", {"request": request, "data": faculty})

# Route to handle POST requests for deleting a faculty member
@app.post("/delete-faculty", response_class=HTMLResponse)
async def delete_faculty_endpoint(Fid: str = Form(...)):
    delete_faculty(Fid)
    faculty = fetch_faculty()  # Fetch updated faculty list after deletion
    return templates.TemplateResponse("index.html", {"request": request, "data": faculty})

from fastapi import FastAPI, HTTPException, Form
@app.post("/get-faculty")
async def get_faculty(Fid: str = Form(...)):
    try:
        conn = sqlite3.connect("Faculty")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Faculty WHERE Fid = ?", (Fid,))
        faculty = cursor.fetchone()
        cursor.close()
        conn.close()
        if faculty:
            return {
                "Name": faculty[0],
                "Department": faculty[1],
                "Fid": faculty[2],
                "Mobile": faculty[3],
                "Email": faculty[4]
            }
        else:
            raise HTTPException(status_code=404, detail="Faculty not found")
    except Exception as e:
        print("Error:", e)  # Print the error for debugging purposes
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/update-faculty")
async def update_faculty(faculty_data: dict):
    try:
        conn = sqlite3.connect("Faculty")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Faculty 
            SET Name = ?, Department = ?, Mobile = ?, Email = ?
            WHERE Fid = ?
            """,
            (faculty_data["Name"], faculty_data["Department"], faculty_data["Mobile"], faculty_data["Email"], faculty_data["Fid"])
        )

        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Faculty details updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating faculty")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

    

# mycursor=mydb.cursor()
# mycursor.execute("use university;")
# str="insert into users(username,email) values('ran','ran@gmail.com');"
# mycursor.execute(str)
# mycursor.execute("select * from users;")
# data=mycursor.fetchall()
# print(data)


# userconn=sqlite3.connect("User")
import mysql.connector
def get_db_connection():
    try:
        myconnection=mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="university"
        )
        return myconnection
    except Exception as e:
        print(e)
        return None

@app.get("/signin")
def read_signin(request: Request):
    return templates.TemplateResponse("Signin.html", {"request": request})

@app.get("/signup")
def read_signup(request: Request):
    return templates.TemplateResponse("SignUp.html", {"request": request}) 

# @app.get("/User-details")
# def User(user_request:Request):   
#     # mycursor.execute('use university;')
#     myconnection=get_db_connection()
#     if not myconnection:
#         return{"Error":"Database connection failed"}

#     try:
#         mycursor=myconnection.cursor()
#         print("Database connected")
#         mycursor.execute("select * from users")
#         users=mycursor.fetchall()
#         print(users)
#         myconnection.commit()
#     except Exception as e:
#         print(e)
#         # mydb.rollback()
#     finally:
#         mycursor.close()
#         myconnection.close()
#     return templates.TemplateResponse("Signin.html", {"request": user_request})
@app.post("/add-user")
def signup(UserName:str=Form(...),Email:str=Form(...),password:str=Form(...)):
    myconnection=get_db_connection()
    if not myconnection:
        return{"Error":"Database connection failed"}
    # mycursor.execute('use university;')
    try:
        mycursor=myconnection.cursor()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        query="insert into users (username,email,password) values (%s,%s,%s) "
        print(query)
        mycursor.execute(query,(UserName,Email,hashed_password))
        myconnection.commit()
        return RedirectResponse(url="/signin", status_code=302)
    except IntegrityError as e:
        print(f"Integrity error: {e}" )
        if e.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
            return {"Error": "Username or email already exists"}
        else:
            return {"Error": str(e)}
    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")  # Log the exception
        return {"Error": str(e)}    
    except Exception as e:
        print(e)
        myconnection.rollback()
    finally:
        mycursor.close()
        myconnection.close()
        # return True

def check_username_exists(mycursor, username):
    query = "SELECT password FROM users WHERE username = %s"
    mycursor.execute(query, (username,))
    result = mycursor.fetchone()
    mycursor.fetchall() # This ensures any remaining results are read and discarded
    return result

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

@app.post("/sign-in")
def signin(UserName:str=Form(...),password:str=Form(...)):
    myconnection=get_db_connection()
    if not myconnection:
        return{"Error":"Database connection failed"}
    try:
        mycursor=myconnection.cursor()
        result = check_username_exists(mycursor, UserName)
        if result:
            stored_password = result[0]
            if verify_password(stored_password, password):
                return {"Success": "Authentication successful"}
            else:
                return {"Error": "Incorrect password"}
        else:
            return {"Error": "Username does not exist"}
        
    except Exception as e:
        print(e)
        # myconnection.rollback()
    finally:
        mycursor.close()
        myconnection.close()
