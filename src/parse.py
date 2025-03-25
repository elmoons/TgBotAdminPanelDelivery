import requests
from urllib import parse
from src.config import settings


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

    if response.status_code == 200:
        data = response.json()
    else:
        data = None

    if data:
        title = data.get("detail", {}).get("title", "")

        # Словарь для хранения лучших конфигураций
        best_configurations = {}

        for sku in data.get("skus", []):
            # Формируем ключ конфигурации (цвет + объем памяти)
            level_1_value = None
            level_2_value = None

            for prop in sku.get("properties", []):
                if prop["level"] == 1:
                    level_1_value = prop["saleProperty"]["value"]
                elif prop["level"] == 2:
                    level_2_value = prop["saleProperty"]["value"]

            config_key = (level_1_value, level_2_value)

            # Находим минимальную цену для этой конфигурации
            min_price = None
            best_price_data = None

            if "price" in sku:
                for price_entry in sku["price"].get("prices", []):
                    current_price = price_entry.get("price")
                    if current_price is not None:
                        if min_price is None or current_price < min_price:
                            min_price = current_price
                            best_price_data = {
                                "tradeType": price_entry.get("tradeType"),
                                "tradeDesc": price_entry.get("tradeDesc"),
                                "price": current_price,
                                "timeDelivery": price_entry.get("timeDelivery"),
                            }

            # Если для этой конфигурации уже есть запись, сравниваем цены
            if config_key in best_configurations:
                if min_price is not None and min_price < best_configurations[config_key]["best_price"]:
                    best_configurations[config_key] = {
                        "sku": sku,
                        "best_price": min_price,
                        "best_price_data": best_price_data
                    }
            elif min_price is not None:
                best_configurations[config_key] = {
                    "sku": sku,
                    "best_price": min_price,
                    "best_price_data": best_price_data
                }

        # Формируем итоговый результат только с лучшими конфигурациями
        result = []
        for config in best_configurations.values():
            sku = config["sku"]
            best_price_data = config["best_price_data"]

            extracted_data = {
                "title": title,
                "logoUrl": sku.get("logoUrl"),
                "level_1": {
                    "name": None,
                    "value": None,
                },
                "level_2": {
                    "name": None,
                    "value": None,
                },
                "prices": [best_price_data] if best_price_data else [],
            }

            for prop in sku.get("properties", []):
                if prop["level"] == 1:
                    extracted_data["level_1"]["name"] = prop["saleProperty"]["name"]
                    extracted_data["level_1"]["value"] = prop["saleProperty"]["value"]
                elif prop["level"] == 2:
                    extracted_data["level_2"]["name"] = prop["saleProperty"]["name"]
                    extracted_data["level_2"]["value"] = prop["saleProperty"]["value"]

            result.append(extracted_data)

        return result
    else:
        raise KeyError
