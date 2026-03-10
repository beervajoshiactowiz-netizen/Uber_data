import sys
import time
import threading
import logging
from utils import read_gzip_range
from parser import parser
from db_config import create, insert_batch,make_connection


FOLDER = r"C:\Users\beerva.joshi\PycharmProjects\new_json\PDP\PDP"
TABLE_NAME = "RestaurantData"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("ubereat.log"),   # saves to file
    ]
)
logger = logging.getLogger(__name__)

BATCH_SIZE = 2000
lock            = threading.Lock()
grand_total     = 0
grand_failed    = 0

def main(thread_id,start, end):
    global grand_total, grand_failed
    batch = []
    total = 0
    failed=0

    conn   = make_connection()
    cursor = conn.cursor()
    for json_data in read_gzip_range(FOLDER, start, end):
        try:

            result = parser(json_data)

            batch.extend(result)
        except Exception as e:
            failed += 1
            continue

        if len(batch) >= BATCH_SIZE:

            insert_batch(TABLE_NAME, batch,conn,cursor)

            total += len(batch)
            logger.info(f"[Thread-{thread_id}] Inserted: {total}")
            batch = []
    if batch:
        insert_batch(TABLE_NAME, batch,conn,cursor)
        total += len(batch)
    cursor.close()
    conn.close()
    logger.info(f"[Thread-{thread_id}] Finished. Inserted: {total} | Failed: {failed}")

    with lock:
        grand_total += total
        grand_failed += failed


if __name__ == "__main__":
    create(TABLE_NAME)


    start_time = time.time()
    threads=[]
    files=122888
    step=25000
    for i in range(0,files,step):
        last=min(i+step,files)
        t=threading.Thread(target=main,args=(i//step+1,i,last))
        threads.append(t)
        t.start()
        logger.info(f"[Thread-{i // step + 1}] Started -> files {i} to {last}")

    for i in threads:
        i.join()


    logger.info(f"Time: {time.time() - start_time:.2f} sec")
