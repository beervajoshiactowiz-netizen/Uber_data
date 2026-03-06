import mysql.connector
import json

def make_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='actowiz',
        database='RestaurantData'
    )
    return conn

def create(table_name: str):
    q = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            RestaurantName  varchar(255),
            RestaurantId varchar(255) unique,
            phoneNo varchar(100),
            Address  varchar(500),
            street  varchar(500),
            city  varchar(500),
            country varchar(100),
            Postalcode varchar(100) ,
            region varchar(100),
            supportedDiningMode Json,
            timing JSON,
            ETA varchar(50),
            CurrencyCode varchar(10),
            Distance varchar(100),
            Cuisines json,
            MenuItems  json
        )
    """
    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute(q)
    conn.commit()
    conn.close()

def insert_batch(table_name, data_list):
    if not data_list:
        return

    conn = make_connection()
    cursor = conn.cursor()

    for data in data_list:
        data["Cuisines"] = json.dumps(data.get("Cuisines"))
        data["supportedDiningMode"] = json.dumps(data.get("supportedDiningMode"))
        data["MenuItems"] = json.dumps(data.get("MenuItems"))
        data["timing"]=json.dumps(data.get("timing"))

    cols = ",".join(data_list[0].keys())

    vals = ",".join(["%s"] * len(data_list[0]))

    q = f"INSERT INTO {table_name} ({cols}) VALUES ({vals})"

    rows = [tuple(d.values()) for d in data_list]

    cursor.executemany(q, rows)

    conn.commit()
    conn.close()

