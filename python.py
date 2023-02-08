import mysql.connector

mydb = mysql.connector.connect(
  host="sql178.main-hosting.eu",
  user="u733493607_pythondb",
  password="python@3NGINE",
  database="u733493607_pythondb"
)

currency = '"EURUSD"'
winAmt = '"100000000"'

cursor = mydb.cursor()

mycursor = mydb.cursor()

sql = (f"UPDATE active SET winAmt = {winAmt} WHERE currency = {currency}" )
mycursor.execute(sql)
mydb.commit()
print(mycursor.rowcount, "record(s) affected")