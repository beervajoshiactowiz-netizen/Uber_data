import re

def parser(json_data):

    if isinstance(json_data, dict):
        json_data = [json_data]

    page = []
    for data in json_data:

        # If an element is string, skip
        if not isinstance(data, dict):
            continue

        base = data.get("data", {})
        if not isinstance(base, dict):
            base = {}

        id = base.get("uuid")
        if not id:
            continue

        result = {}

        location = base.get("location", {}) or {}

        result["RestaurantName"] = base.get("title")
        result["RestaurantId"] = base.get("uuid")
        result["phoneNo"] = base.get("phoneNumber")
        result["Address"] = location.get("address")
        result["street"] = location.get("streetAddress")
        result["city"] = location.get("city")
        result["country"] = location.get("country")
        result["Postalcode"] = location.get("postalCode")
        result["region"] = location.get("region")

        # ETA
        eta_raw = (base.get("etaRange") or {}).get("text") or ""
        eta_num = re.findall(r"\d+", eta_raw)
        if len(eta_num) >= 2:
            result["ETA"] = f"{eta_num[0]} to {eta_num[1]} min"
        else:
            result["ETA"] = None

        # Timing
        timing = {}
        for h in base.get("hours", []):
            days = [d.strip() for d in h.get("dayRange", "").split("-")]
            times = h.get("sectionHours", [])
            value = "Closed" if not times else [
                f"{to_time(t['startTime'])}-{to_time(t['endTime'])}" for t in times
            ]
            for d in days:
                timing[d] = value if len(value or []) > 1 else (value[0] if value else None)
        result["timing"] = timing

        result["CurrencyCode"] = base.get("currencyCode")
        result["Cuisines"] = base.get("cuisineList")
        result["Distance"] = (base.get("distanceBadge") or {}).get("accessibilityText")
        result["supportedDiningMode"] = [
            m.get("mode")
            for m in base.get("supportedDiningModes", [])
            if m.get("isAvailable")
        ]

        # Menu items
        result["MenuItems"] = []
        categories = (
            base.get("catalogSectionsMap", {}) or {}
        ).get("0ad5db85-c10f-5ad6-897c-f8ef6bd5cc78", [])

        for category in categories:
            temp = {}
            payload = category.get("payload") or {}
            itempayload = payload.get("standardItemsPayload") or {}
            temp["category"] = (itempayload.get("title") or {}).get("text")

            items_out = []
            for item in itempayload.get("catalogItems", []):
                price_tag = item.get("priceTagline") or {}
                items_out.append({
                    "itemName": item.get("title"),
                    "itemId": item.get("uuid"),
                    "itemDescription": item.get("itemDescription"),
                    "itemPrice": price_tag.get("text"), 
                    "imageUrl": item.get("imageUrl"),
                })
            temp["items"] = items_out
            result["MenuItems"].append(temp)

        page.append(result)
    return page


def to_time(m):
    return f"{m // 60:02d}:{m % 60:02d}"
