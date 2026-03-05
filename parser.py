import json
from db_config import create, insert_into_db
import re
from pprint import pprint
import time
from utils import read_files
from model import RestaurantModel

DIR_PATH = r"C:\Users\beerva.joshi\Downloads\000a5dc6-cf5f-5967-b29a-d581e8f39339.json"
TABLE_NAME = 'RestaurantData'

def parser(json_data):
    result = {}
    base=json_data.get("data",{})
    location=base.get("location",{})

    result["RestaurantName"]=base.get("title")
    result["RestaurantId"]=base.get("uuid")
    result["phoneNo"]=base.get("phoneNumber")
    result["Address"]=location.get("address")
    result["street"]=location.get("streetAddress")
    result["city"]=location.get("city")
    result["country"]=location.get("country")
    result["Postalcode"]=location.get("postalCode")
    result["region"]=location.get("region")
    eta=base.get("etaRange",{}).get("text")
    eta_num=re.findall(r"\d+",eta)

    timing = {}
    for h in base.get("hours", []):
        days = [d.strip() for d in h.get("dayRange", "").split("-")]
        times = h.get("sectionHours", [])
        value = "Closed" if not times else [
            f"{to_time(t['startTime'])}-{to_time(t['endTime'])}" for t in times
        ]
        for d in days:
            timing[d] = value if len(value or []) > 1 else (value[0] if value else None)
    result["timing"]=timing

    if len(eta_num) == 2:
        eta_clean = f"{eta_num[0]} to {eta_num[1]} min"
    else:
        eta_clean = None
    result["ETA"]=eta_clean
    result["CurrencyCode"]=base.get("currencyCode")
    result["Cuisines"]=base.get("cuisineList")
    result["Distance"]=base.get("distanceBadge",{}).get("accessibilityText")
    result["supportedDiningMode"]=[m.get("mode")
                                   for m in base.get("supportedDiningModes", [])
                                   if m.get("isAvailable")]
    result["MenuItems"]=[]

    for category in base.get("catalogSectionsMap").get('0ad5db85-c10f-5ad6-897c-f8ef6bd5cc78'):

        temp = {}
        itempayload=category.get("payload").get("standardItemsPayload")
        temp["category"]=itempayload.get("title",{}).get("text")

        item=[]
        for items in itempayload.get("catalogItems",[]):
            item.append({
                "itemName":items.get("title"),
                "itemId":items.get("uuid"),
                "itemDescription":items.get("itemDescription"),
                "itemPrice":items.get("priceTagline").get("text"),
                "imageUrl":items.get("imageUrl")
        })
        temp["items"]=item
        result["MenuItems"].append(temp)

    return result

def to_time(m):
    return f"{m//60:02d}:{m%60:02d}"

def main():
    create(TABLE_NAME)
    raw_data = read_files(DIR_PATH)
    result=parser(raw_data)
    try:
        validated = RestaurantModel(**result)
        clean_data = validated.model_dump()
        insert_into_db(TABLE_NAME,clean_data)
    except Exception as e:
        print("Validation Failed:", e)

if __name__ == '__main__':
    st = time.time()
    main()
    tt = time.time() - st
    print(tt)