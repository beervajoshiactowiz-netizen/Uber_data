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
            RestaurantId varchar(255),
            phoneNo varchar(100),
            Address  varchar(100),
            street  varchar(255),
            city  varchar(100),
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


def insert_into_db(table_name: str, data: dict):
    for k, v in data.items():
        if isinstance(v, (list, dict)):
            data[k] = json.dumps(v)
    cols = ",".join(list(data.keys()))
    vals = "".join([len(data.keys()) * '%s,']).strip(',')
    q = f"INSERT INTO {table_name} ({cols}) VALUES ({vals})"
    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute(q, tuple(data.values()))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    pass