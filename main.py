import json
import os

FILE_DATA = "pocketbudget_data.json"

def muat_data() :
    if os.path.exists(FILE_DATA):
        with open(FILE_DATA, "r") as file:
            return json.load(file)
    return {"saldo": 0, "transaksi": []}

def simpan_data(data):
    with open(FILE_DATA, "w") as file:
        json.dump(data, file, indent=4)

  
