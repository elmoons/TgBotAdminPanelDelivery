import logging

import requests
from urllib import parse
from src.config import settings
from src.exceptions import PoizonAPIError

USED_PRODUCTS = ["堪比新机", "自用首选"]


def get_spuid(product_link: str):
    query = parse.urlparse(product_link).query
    spuid = parse.parse_qs(query)["spuId"][0]
    if spuid is None:
        raise ValueError("SpuId is None")
    return spuid


def get_data_about_product(spuId: int):
    headers = {"apiKey": settings.POIZON_API_KEY}
    params = {"spuId": spuId}

    response = requests.get(
        url="https://poizon-api.com/api/dewu/productDetailWithPrice",
        params=params,
        headers=headers,
    )

    if response.status_code == 400:
        raise PoizonAPIError

    if response.status_code != 200:
        raise KeyError(f"API Error: {response.status_code}")

    data = response.json()
    if not data:
        return []

    title = data.get("detail", {}).get("title", "")
    best_configs = {}

    for sku in data.get("skus", []):
        color = None
        memory = None
        level_1_name = None
        level_2_name = None

        for prop in sku.get("properties", []):
            if prop["level"] == 1:
                color = prop["saleProperty"]["value"]
                level_1_name = prop["saleProperty"]["name"]
            elif prop["level"] == 2:
                memory = prop["saleProperty"]["value"]
                level_2_name = prop["saleProperty"]["name"]

        if not color or not memory:
            continue

        config_key = (color, memory)
        min_price_entry = None

        for price_entry in sku.get("price", {}).get("prices", []):
            # Пропускаем б/у товары
            if price_entry.get("tradeDesc") in USED_PRODUCTS:
                continue

            price = price_entry.get("price")
            if price is None:
                continue

            if (min_price_entry is None) or (price < min_price_entry["price"]):
                min_price_entry = {
                    "tradeType": price_entry.get("tradeType"),
                    "tradeDesc": price_entry.get("tradeDesc"),
                    "price": price,
                    "timeDelivery": price_entry.get("timeDelivery"),
                }

        if not min_price_entry:
            continue

        if (config_key not in best_configs) or (
            min_price_entry["price"] < best_configs[config_key]["min_price"]
        ):
            best_configs[config_key] = {
                "min_price": min_price_entry["price"],
                "logoUrl": sku.get("logoUrl"),
                "level_1_name": level_1_name,
                "level_2_name": level_2_name,
                "price_entry": min_price_entry,
            }

    return [
        {
            "title": title,
            "logoUrl": config["logoUrl"],
            "level_1": {"name": config["level_1_name"], "value": color},
            "level_2": {"name": config["level_2_name"], "value": memory},
            "prices": [config["price_entry"]],
        }
        for (color, memory), config in best_configs.items()
    ]
