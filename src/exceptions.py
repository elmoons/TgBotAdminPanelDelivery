class NotDataAboutPrice(Exception):
    detail = ("Данные для ценообразования небыли установлены.\n"
              "Установите их по команде /change_data_price.")