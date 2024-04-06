import sqlite3
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from requests import request


conn=sqlite3.connect("Faculty")
cursor=conn.cursor()
try:
    conn.execute('BEGIN')
    conn.commit()
except Exception as e:
    print(e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()   

app=FastAPI()
templates=Jinja2Templates(directory="templates")
@app.get("/Faculty-details")
def Faculty(request:Request):
    conn=sqlite3.connect("Faculty")
    cursor=conn.cursor()
    try:
        conn.execute('BEGIN')
        cursor.execute("select * from Faculty")
        Faculty=cursor.fetchall()
        print(Faculty)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
    return templates.TemplateResponse("index.html", {"request": request,"data": Faculty})

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