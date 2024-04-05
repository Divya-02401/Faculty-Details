import sqlite3
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from requests import request


conn=sqlite3.connect("Faculty")
cursor=conn.cursor()
try:
    conn.execute('BEGIN')
    # cursor.execute('drop table Faculty')
    # cursor.execute("create table Faculty ('Name' vachar2(20), 'Department' varchar2(30) , 'Fid' number(10), 'Mobile' number(10), 'Email' varchar2(50))")
    # cursor.execute("insert into Faculty Values ('Lakshmi','Maths',1214008,123567891,'lakshmi@gmail.com')")
    # cursor.execute("insert into Faculty values('Vijaya','Stats',1214010,1231231231,'vijaya@gmail.com')")
    # cursor.execute("insert into Faculty Values ('Rani','Computers',1214009,123567891,'rani@gmail.com')")
    # cursor.execute("insert into Faculty Values ('Priya','English',1214016,1234561234,'priya@gmail.com')")
    # cursor.execute("insert into Faculty Values ('Keerthi','Maths',1214001,1212121212,'keerthi@gmail.com')")
    # cursor.execute("insert into Faculty Values ('Rakesh','Physics',1214003,1234512345,'rakesh@gmail.com')")
    # cursor.execute("insert into Faculty Values ('Aishu','Chemistry',1214005,1234123412,'aishu@gmail.com')")
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

