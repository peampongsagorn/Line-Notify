import requests
import pymssql
from discord_webhook import DiscordWebhook

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


data = message

webhook_url = "Place WebHook URL Here"


webhook = DiscordWebhook(url = webhook_url, content = data)
response = webhook.execute()

print(response.status_code) 
