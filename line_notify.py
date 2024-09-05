import requests
import pymssql

server = "your_server_ip"
user = "username_database"
password = "password_database"
database = "database_name"

conn = pymssql.connect(server, user, password,database)
cursor = conn.cursor()

query = """
place your query here
"""
cursor.execute(query)
rows = cursor.fetchall()

conn.close()
print (rows)

for row in rows:
    column_name_1 = row[0]
    column_name_2 = row[1]
    column_name_3 = row[2]
    # Add more column names as needed

message = (
    f"Place Job Name Here\n"
    f"Database: Place Database Name Here\n"
    f"Table :  Place Table Name Here\n"
    f"column_name_1: {column_name_1}\n"
    f"column_name_2: {column_name_2}\n"
    f"column_name_3: {column_name_3}\n"
)

token = "Place Line Token Here"
url = "https://notify-api.line.me/api/notify"
headers = {
    'Content-Type' : 'application/x-www-form-urlencoded',
    "Authorization": f"Bearer {token}",
}
data = {
    "message": message,
    # "stickerPackageId": 6632,
    # "stickerId": 11825374,
}



response = requests.post(url, headers=headers, data=data)
print(f"Status: {response.status_code}, Response: {response.text}")
