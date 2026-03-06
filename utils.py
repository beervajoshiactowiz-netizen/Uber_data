import os
import json
import gzip

def read_files(path: str):
    with open(path,"r") as f:
        data=json.load(f)
        return data

def read_gzip_range(FOLDER, start, end):
    files = sorted(os.listdir(FOLDER))

    for file in files[start:end]:
        path = os.path.join(FOLDER, file)

        try:
            with gzip.open(path, "rt", encoding="utf-8") as f:
                data=json.load(f)
                yield data

        except Exception as e:
            print("File error:", file, e)
