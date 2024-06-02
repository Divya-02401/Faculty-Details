import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database='university'
)

try:
    mycursor=mydb.cursor()
    # mycursor.execute("use university;")
    str="insert into users(username,email) values('div','div@gmail.com');"
    mycursor.execute(str)
    mycursor.execute("select * from users;")
    data=mycursor.fetchall()
    print(data)
    mydb.commit()  # Commit the transaction
    print("Data inserted successfully")
except mysql.connector.Error as error:
    print(f"Failed to insert data: {error}")
    mydb.rollback()  # Rollback the transaction in case of error
finally:
    mycursor.close()
    mydb.close()