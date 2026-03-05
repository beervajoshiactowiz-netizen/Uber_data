import os
import json
import gzip


def read_files(path: str):
    with open(path,"r") as f:
        data=json.load(f)
        return data

def read_files_zip(path: str):
    try:
        files = os.listdir(path)
        for file in files:
            filename = os.path.join(path, file)
            content = gzip.open(filename).read()
            yield json.loads(content)
    except Exception as e:
        print("Error in func:", read_files.__name__, '\nError: ', e)


