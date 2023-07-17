import mysql.connector
# Establish the database connection
class db():
     db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='email'
  )