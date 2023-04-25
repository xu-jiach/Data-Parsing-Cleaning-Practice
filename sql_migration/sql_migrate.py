import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    port = 3306,
    user="root",
    password="0510",
    database="badminton"
)

cursor = mydb.cursor()

cursor.execute("DROP TABLE IF EXISTS minatoku")

cursor.execute("""
    CREATE TABLE minatoku (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        year INT,
        url VARCHAR(255)
    )
""")

with open('D:\python-project\Badminton_scheduling\sql_migration\schedule_sql.txt', 'r') as f:
    for line in f:
        data = line.strip().split(', ')
        title, year, url, id_ = data
        sql = "INSERT INTO minatoku (title, year, url, id) VALUES (%s, %s, %s, %s)"
        val = (title, year, url, id_)
        cursor.execute(sql, val)
        mydb.commit()

mydb.commit()
mydb.close()

