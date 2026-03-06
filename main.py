import sys
import time

from utils import read_gzip_range
from parser import parser
from db_config import create, insert_batch


FOLDER = r"C:\Users\beerva.joshi\PycharmProjects\new_json\PDP\PDP"
TABLE_NAME = "RestaurantData"

BATCH_SIZE = 2000

def main(start, end):

    batch = []
    total = 0

    for json_data in read_gzip_range(FOLDER, start, end):

        result = parser(json_data)

        batch.extend(result)

        if len(batch) >= BATCH_SIZE:

            insert_batch(TABLE_NAME, batch)

            total += len(batch)

            print("Inserted:", total)

            batch = []
    if batch:
        insert_batch(TABLE_NAME, batch)
        total += len(batch)

    print("Finished. Total inserted:", total)


if __name__ == "__main__":
    create(TABLE_NAME)

    start = int(sys.argv[1])
    end = int(sys.argv[2])

    start_time = time.time()

    main(start, end)

    print("Total Time:", time.time() - start_time)