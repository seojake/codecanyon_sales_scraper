import mysql.connector

db_conn = mysql.connector.connect(
    user='root', ## DB User
    password='root', ## DB Password
    host='localhost:8888', ## DB Hostname
    database='codecanyon', ## Database name (don't forget to change this)
    unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock' ## Remove this if you don't need to use a socket
)

db_exe = db_conn.cursor()
