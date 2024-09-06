import requests
import pymssql

server = "192.168.132.46"
user = "sa"
password = "Ny#Z!{o&p%>07"
database = "HealthIDDynamic_UAT"

conn = pymssql.connect(server, user, password, database)
cursor = conn.cursor()

query = """
SELECT 
    dbschemas.[name] AS [Schema],
    dbtables.[name] AS [Table],
    dbindexes.[name] AS [Index],
    indexstats.avg_fragmentation_in_percent
FROM 
    sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') AS indexstats
    INNER JOIN sys.tables dbtables ON dbtables.[object_id] = indexstats.[object_id]
    INNER JOIN sys.schemas dbschemas ON dbtables.[schema_id] = dbschemas.[schema_id]
    INNER JOIN sys.indexes dbindexes ON dbindexes.[object_id] = indexstats.[object_id]
       AND indexstats.index_id = dbindexes.index_id
WHERE 
    where dbindexes.[name] is not null
ORDER BY 
    indexstats.avg_fragmentation_in_percent DESC;
"""
cursor.execute(query)
rows = cursor.fetchall()

conn.close()

if rows:
    token = "6heZZeNcO91nB5cHZPrTiWurWCjfRam8NhbADFlrLpp"
    url = "https://notify-api.line.me/api/notify"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "Authorization": f"Bearer {token}",
    }

    for row in rows:
        schema_name = row[0]
        table_name = row[1]
        index_name = row[2]
        fragmentation_percent = row[3]

        message = (
            f"Fragmentation Alert\n"
            f"Database: {database}\n"
            f"Schema: {schema_name}\n"
            f"Table: {table_name}\n"
            f"Index: {index_name}\n"
            f"Fragmentation: {fragmentation_percent:.2f}%\n"
        )

        data = {
            "message": message,
        }

        response = requests.post(url, headers=headers, data=data)
        print(f"Status: {response.status_code}, Response: {response.text}")
else:
    print("No indexes with fragmentation above 30%. No message sent.")
