from http.client import HTTPException
import sqlite3
import bcrypt
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from requests import request

app=FastAPI()
templates=Jinja2Templates(directory="templates")

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

myconnection=get_db_connection()
mycursor=myconnection.cursor()



@app.get('/Faculty-details',response_class=HTMLResponse)
def Faculty(request:Request):
    myconnection=get_db_connection()
    mycursor=myconnection.cursor()
    Faculty_details=[]
    try:   
        mycursor.execute("select * from Faculty")
        Faculty_details=mycursor.fetchall()
        print(Faculty_details)
        myconnection.commit()
    except mysql.connector.Error as e:
        print(e)
        # Faculty_details = []
    except Exception as e:
        print(e)
        # conn.rollback()
        # Faculty_details=[]
    finally:
        mycursor.close()
        myconnection.close()
    return templates.TemplateResponse("index.html", {"request": request,"data": Faculty_details})

@app.post('/add-faculty')
def add_faculty(Name:str=Form(...),Department:str=Form(...),Fid:str=Form(...),Mobile:str=Form(...),Email:str=Form(...)):
    myconnection=get_db_connection()
    if not myconnection:
        return {"error": "Failed to connect to the database"}
    mycursor=myconnection.cursor()
    try:
        query="insert into Faculty (Name,Department,Fid,Mobile,Email) values(%s,%s,%s,%s,%s)"
        # myconnection.execute('BEGIN')
        values=(Name,Department,Fid,Mobile,Email)
        print(query % values)
        mycursor.execute(query,values)
        myconnection.commit()
    except Exception as e:
        print(e)
        myconnection.rollback()
    finally:
        mycursor.close()
        myconnection.close()
    return True

# @app.post("/delete-faculty")
# def delete_faculty(Fid:str=Form(...)):
#     myconnection=get_db_connection()
#     mycursor=myconnection.cursor()
#     try:
#         query=f"delete from Faculty where (Fid) = ('{Fid}')"
#         print(query)
#         # myconnection.execute('BEGIN')
#         mycursor.execute(query)
#         myconnection.commit()
#     except Exception as e:
#         print(e)
#         myconnection.rollback()
#     finally:
#         mycursor.close()
#         myconnection.close()
#     return True


@app.get("/departments")
async def get_departments():
    myconnection=get_db_connection()
    if not myconnection:
        return {"error": "Failed to connect to the database"}
    mycursor=myconnection.cursor()
    try:
        query = "SELECT DISTINCT Department FROM Faculty"
        mycursor.execute(query)
        departments = [row[0] for row in mycursor.fetchall()]
        return departments
    except Exception as e:
        print("Error fetching departments:", e)
        return []
    finally:
        mycursor.close()
        myconnection.close()

@app.post("/select-department")
async def search_department(request: Request, Department: dict):
    myconnection=get_db_connection()
    if not myconnection:
        return {"error": "Failed to connect to the database"}
    mycursor=myconnection.cursor()
    selected_department = Department.get('Department')
    try:
        query="SELECT *  FROM Faculty where Department= %s "

        print(query)
        # myconnection.execute('BEGIN')
        mycursor.execute(query,(selected_department,)) 
        Faculty=mycursor.fetchall()
        print(Faculty)
        myconnection.commit()
    except Exception as e:
        myconnection.rollback()
    finally:
        mycursor.close()
        myconnection.close()  
    return Faculty



# Define a function to fetch all faculty members
def fetch_faculty():
    myconnection=get_db_connection()
    if not myconnection:
        return {"error": "Failed to connect to the database"}
    mycursor=myconnection.cursor()
    try:
        mycursor.execute("SELECT * FROM Faculty")
        faculty = mycursor.fetchall()
        return faculty
    finally:
        mycursor.close()
        myconnection.close()

# Define a function to delete a faculty member by their Fid
def delete_faculty(Fid:str):
    myconnection=get_db_connection()
    if not myconnection:
        return {"error": "Failed to connect to the database"}
    mycursor=myconnection.cursor()
    try:
        query="DELETE FROM Faculty WHERE Fid=%s"
        mycursor.execute(query,(Fid,))
        myconnection.commit()
        return {"message": "Faculty deleted successfully"}
    except Exception as e:
        print("Error deleting faculty:", e)
        raise HTTPException(status_code=500, detail="Failed to delete faculty")
    finally:
        mycursor.close()
        myconnection.close()
        
# Route to handle GET requests for displaying faculty details
@app.get("/Faculty-details", response_class=HTMLResponse)
async def display_faculty(request: Request):
    faculty = fetch_faculty()
    return templates.TemplateResponse("index.html", {"request": request, "data": faculty})

# Route to handle POST requests for deleting a faculty member
@app.post("/delete-faculty", response_class=HTMLResponse)
async def delete_faculty_endpoint(request: Request):
    form_data = await request.form()
    Fid = form_data.get('Fid')
    delete_faculty(Fid)
    faculty = fetch_faculty()  # Fetch updated faculty list after deletion
    return templates.TemplateResponse("index.html", {"request": request, "data": faculty})

from fastapi import FastAPI, HTTPException, Form
@app.post("/get-faculty")
async def get_faculty(Fid: str = Form(...)):
    myconnection=get_db_connection()
    if not myconnection:
        return {"error": "Failed to connect to the database"}
    mycursor=myconnection.cursor()
    try:
        
        mycursor.execute("SELECT * FROM Faculty WHERE Fid = %s", (Fid,))
        faculty = mycursor.fetchone()
        # mycursor.fetchall()
        mycursor.close()
        myconnection.close()
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
    myconnection=get_db_connection()
    if not myconnection:
        return {"error": "Failed to connect to the database"}
    mycursor=myconnection.cursor()
    try:
        mycursor.execute("""
            UPDATE Faculty 
            SET Name = %s, Department = %s, Mobile = %s, Email = %s
            WHERE Fid = %s
            """,
            (faculty_data["Name"], faculty_data["Department"], faculty_data["Mobile"], faculty_data["Email"], faculty_data["Fid"])
        )

        myconnection.commit()
        mycursor.close()
        myconnection.close()

        return {"message": "Faculty details updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating faculty")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/signin")
def read_signin(request: Request):
    return templates.TemplateResponse("Signin.html", {"request": request})

@app.get("/signup")
def read_signup(request: Request):
    return templates.TemplateResponse("SignUp.html", {"request": request}) 

@app.get("/User-details",response_class=HTMLResponse)
def User(user_request:Request):   
    myconnection=get_db_connection()
    if not myconnection:
        return{"Error":"Database connection failed"}
    mycursor=myconnection.cursor()
    users=[]

    try:
        mycursor.execute("select id,username,email,Type from users")
        users=mycursor.fetchall()
        print(users)
        myconnection.commit()
    except Exception as e:
        print(e)
        # mydb.rollback()
    finally:
        mycursor.close()
        myconnection.close()
    return templates.TemplateResponse("User.html", {"request": user_request,"data":users})


@app.post("/add-user")
def signup(UserName:str=Form(...),Email:str=Form(...),password:str=Form(...)):
    myconnection=get_db_connection()
    if not myconnection:
        return{"Error":"Database connection failed"}
    # mycursor.execute('use university;')
    try:
        mycursor=myconnection.cursor()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        query="insert into users (username,email,password,Type) values (%s,%s,%s,%s) "
        print(query)
        mycursor.execute(query,(UserName,Email,hashed_password,"Faculty"))
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
    query = "SELECT password, Type FROM users WHERE username = %s"
    mycursor.execute(query, (username,))
    result=mycursor.fetchone()
    mycursor.fetchall()
    return result

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))


# def get_user_type(username: str):
#     # This function should query the database to get the type of the user
#     # Replace this with your actual database query logic
#     # For demonstration purposes, let's assume the user type is stored in a table called 'Users' with a column called 'type'
#     # You should modify this function according to your database schema
#     myconnection = get_db_connection()
#     if not myconnection:
#         raise HTTPException(status_code=500, detail="Failed to connect to the database")
#     mycursor = myconnection.cursor()
#     try:
#         query = "SELECT Type FROM Faculty WHERE Name = %s"
#         mycursor.execute(query, (username,))
#         result = mycursor.fetchone()
#         if result:
#             return result[0]  # Return the user type
#         else:
#             return None  # If user not found
#     except Exception as e:
#         print("Error:", e)
#         raise HTTPException(status_code=500, detail="Internal Server Error")
#     finally:
#         mycursor.close()
#         myconnection.close()

def get_faculty_details(mycursor, username):
    try:
        query = """
            SELECT f.Name, f.Department, f.Fid, f.Mobile, f.Email
            FROM Faculty f
            INNER JOIN users u ON f.Email = u.email
            WHERE u.username = %s
            """        
        mycursor.execute(query, (username,))
        faculty_details = mycursor.fetchone()
        mycursor.fetchall()
        print("Query details:", faculty_details)
        if faculty_details:
            # If faculty details are found, return them as a dictionary
            return {
                "Name": faculty_details[0],
                "Department": faculty_details[1],
                "Fid": faculty_details[2],
                "Mobile": faculty_details[3],
                "Email": faculty_details[4]
            }
        else:
            # If no details found, return a message or handle as per your requirement
            # return {"message": "Faculty details not found"}
            return None
    except Exception as e:
        print("Error fetching faculty details:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch faculty details")


@app.get("/faculty-details/{username}", response_class=HTMLResponse)
def display_faculty_details(request: Request, username: str):
    myconnection = get_db_connection()
    if not myconnection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    mycursor = myconnection.cursor()

    try:
        faculty_details = get_faculty_details(mycursor, username)
        if faculty_details:
            return templates.TemplateResponse("FacultyDetails.html", {"request": request, "data": faculty_details})
        else:
            return templates.TemplateResponse("FacultyDetails.html", {"request": request, "error": "Details not found"})
    except HTTPException as e:
        raise e  # Propagate HTTP exceptions
    except Exception as e:
        print("Error fetching faculty details:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch faculty details")
    finally:
        mycursor.close()
        myconnection.close()


@app.post("/sign-in")
def signin(UserName:str=Form(...),password:str=Form(...)):
    myconnection=get_db_connection()
    if not myconnection:
        return{"Error":"Database connection failed"}
    mycursor=myconnection.cursor()

    try:
        result = check_username_exists(mycursor, UserName)
        if result:
            stored_password, Type = result  # Assuming the user type is retrieved along with the password
            if verify_password(stored_password, password):
            
                if Type == "Admin":
                    # If user is admin, return faculty table
                    return RedirectResponse(url="/Faculty-details", status_code=302)
                elif Type == "Faculty":
                      # If user is faculty, return True
                    # faculty_details = get_faculty_details(mycursor, UserName)
                    return RedirectResponse(url=f"/faculty-details/{UserName}", status_code=302)
                else:
                    raise HTTPException(status_code=403, detail="Invalid user type")
            else:
                # return templates.TemplateResponse("Signin.html", {"request": request, "error": "Incorrect password"})
                return {"Incorect password"}
        else:
            # return templates.TemplateResponse("Signin.html", {"request": request, "error": "Username doesn't exist"})
            return {"User Name does not exists!"}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        mycursor.close()
        myconnection.close()


@app.get("/get-user/{user_id}")
async def get_user(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, username, email, type FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user:
        return {"id": user[0], "username": user[1], "email": user[2], "type": user[3]}
    return JSONResponse(status_code=404, content={"message": "User not found"})

@app.post("/update-user")
async def update_user(id: int = Form(...), username: str = Form(...), email: str = Form(...), type: str = Form(...)):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE users SET username = %s, email = %s, type = %s WHERE id = %s
    """, (username, email, type, id))
    connection.commit()
    cursor.close()
    connection.close()
    return JSONResponse(status_code=200, content={"success": True})