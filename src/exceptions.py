class NotDataAboutPrice(Exception):
    detail = (
        "Данные для ценообразования небыли установлены.\n"
        "Установите их по команде: /change_data_price."
    )


class NotDataAboutProducts(Exception):
    detail = (
        "Ни один товар не был добавлен.\n"
        "Добавьте товары по команде: /add_poizon_product."
    )


class PoizonAPIError(Exception):
    detail = (
        "Ошибка PoizonAPI, возможно в данный момент сервер недоступен "
        "или на балансе закончились средства."
    )
