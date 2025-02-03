import json
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
        print(f"Ошибка при запросе: {response.status_code}")
        data = None

    if data:
        # Получение общего title из "detail"
        title = data.get("detail", {}).get("title", "")

        # Обработка списка конфигураций
        result = []
        for sku in data.get("skus", []):  # Защита от отсутствия ключа "skus"
            extracted_data = {
                "title": title,  # Добавляем общий title
                "logoUrl": sku.get("logoUrl"),
                "level_1": {
                    "name": None,
                    "value": None,
                },
                "level_2": {
                    "name": None,
                    "value": None,
                },
                "prices": [],  # Список цен и сроков доставки
            }

            # Обрабатываем свойства
            for prop in sku.get(
                "properties", []
            ):  # Защита от отсутствия ключа "properties"
                if prop["level"] == 1:
                    extracted_data["level_1"]["name"] = prop["saleProperty"]["name"]
                    extracted_data["level_1"]["value"] = prop["saleProperty"]["value"]
                elif prop["level"] == 2:
                    extracted_data["level_2"]["name"] = prop["saleProperty"]["name"]
                    extracted_data["level_2"]["value"] = prop["saleProperty"]["value"]

            # Обрабатываем цены
            if "price" in sku:
                for price_entry in sku["price"].get("prices", []):
                    price_data = {
                        "tradeType": price_entry.get("tradeType"),
                        "tradeDesc": price_entry.get("tradeDesc"),
                        "price": price_entry.get("price"),
                        "timeDelivery": price_entry.get("timeDelivery"),
                    }
                    extracted_data["prices"].append(price_data)

            result.append(extracted_data)

        # Вывод всех конфигураций
        return json.dumps(result, indent=4, ensure_ascii=False)
    else:
        raise KeyError
