from pydantic import BaseModel
from typing import List, Optional


class MenuItem(BaseModel):
    itemName: Optional[str]
    itemId: Optional[str]
    itemDescription: Optional[str]
    itemPrice: Optional[str]
    imageUrl: Optional[str]


class Category(BaseModel):
    category: Optional[str]
    items: List[MenuItem] = []


class RestaurantModel(BaseModel):

    RestaurantName: Optional[str]
    RestaurantId: Optional[str]

    phoneNo: Optional[str]

    Address: Optional[str]
    street: Optional[str]
    city: Optional[str]
    country: Optional[str]
    Postalcode: Optional[str]
    region: Optional[str]

    ETA: Optional[str]
    CurrencyCode: Optional[str]

    Distance: Optional[str]

    Cuisines: Optional[List[str]] = []

    supportedDiningMode: Optional[List[str]] = []

    MenuItems: Optional[List[Category]] = []