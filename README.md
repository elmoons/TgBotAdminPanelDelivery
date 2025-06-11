# Telegram Bot Admin Panel for Poizon Price Tracking




## Описание Проекта

Этот Telegram-бот представляет собой административную панель для отслеживания цен на товары с платформы Poizon. Он позволяет администраторам добавлять и удалять товары, а также автоматически обновлять их цены и сохранять данные в Google Таблицах. Проект разработан с использованием современных технологий и обеспечивает удобное управление данными о товарах.

## Ключевые Особенности

*   **Добавление товаров:** Легкое добавление новых товаров с Poizon по ссылке.
*   **Удаление товаров:** Возможность удаления товаров из отслеживания.
*   **Автоматическое обновление цен:** Цены на товары автоматически обновляются в фоновом режиме, отслеживая лучшие предложения только для *новых* товаров (без учета б/у).
*   **Интеграция с Google Sheets:** Все данные о товарах и ценах сохраняются и синхронизируются с Google Таблицами.
*   **Гибкая настройка ценообразования:** Возможность изменения параметров ценообразования (стоимость доставки, курс валют, коэффициент наценки).
*   **Удобный интерфейс:** Интуитивно понятный Telegram-бот для администраторов.

## Используемые Технологии

*   **Python:** Основной язык разработки.
*   **aiogram:** Фреймворк для создания Telegram-ботов.
*   **SQLAlchemy:** ORM для работы с базой данных.
*   **PostgreSQL:** Реляционная база данных для хранения информации о товарах.
*   **Redis:** Брокер сообщений для Celery.
*   **Celery:** Распределенная система очередей задач для фонового обновления цен.
*   **gspread:** Библиотека для работы с Google Sheets API.
*   **Docker/Docker Compose:** Для контейнеризации и управления сервисами.
*   **Alembic:** Инструмент для миграции баз данных.

### Интеграция с Poizon API

Для получения данных о товарах с Poizon используется сторонний API-сервис [poizon-api.com](https://poizon-api.com/). Важно отметить, что у Poizon нет официального публичного API, и данный сервис является хорошим решением для получения актуальных данных, несмотря на то, что он не является бесплатным.




## Установка и Запуск

Для запуска проекта вам потребуется установленный Docker и Docker Compose.

1.  **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/elmoons/TgBotAdminPanelDelivery.git
    cd TgBotAdminPanelDelivery
    ```

2.  **Настройте переменные окружения:**

    Создайте файл `.env` в корневой директории проекта на основе `credentials-example.json` и заполните его своими данными:

    ```
    BOT_TOKEN=ВАШ_ТОКЕН_БОТА
    ADMIN_ID=ВАШ_ID_АДМИНА
    GOOGLE_SHEETS_CREDENTIALS_PATH=/app/credentials.json
    ```

    *   `BOT_TOKEN`: Токен вашего Telegram бота, полученный от BotFather.
    *   `ADMIN_ID`: Ваш Telegram ID для доступа к админ-панели.
    *   `GOOGLE_SHEETS_CREDENTIALS_PATH`: Путь к файлу учетных данных Google Sheets (подробнее см. ниже).

3.  **Настройка Google Sheets API:**

    *   Перейдите в Google Cloud Console и создайте новый проект.
    *   Включите Google Sheets API и Google Drive API.
    *   Создайте учетную запись службы (Service Account) и сгенерируйте ключ в формате JSON. Переименуйте скачанный файл в `credentials.json`.
    *   Поместите файл `credentials.json` в директорию `src/` вашего проекта.
    *   Предоставьте доступ к вашей Google Таблице для email адреса вашей сервисной учетной записи.

4.  **Запуск проекта с помощью Docker Compose:**

    ```bash
    docker-compose up --build -d
    ```

    Эта команда соберет образы и запустит все необходимые сервисы: базу данных PostgreSQL, Redis, Telegram бота и Celery воркеры.




## Структура Проекта

```
TgBotAdminPanelDelivery/
├── Dockerfile
├── README.md
├── alembic.ini
├── credentials-example.json
├── docker-compose.yml
├── requirements.txt
└── src/
    ├── __init__.py
    ├── bot.py
    ├── config.py
    ├── connectors/
    │   └── __init__.py
    ├── database/
    │   ├── __init__.py
    │   ├── database.py
    │   └── models.py
    ├── exceptions.py
    ├── main.py
    ├── migrations/
    ├── parse.py
    ├── sheets.py
    ├── tasks/
    │   ├── __init__.py
    │   ├── celery_app.py
    │   └── tasks.py
    └── utils.py
```

## Использование Бота

После успешного запуска бота вы можете взаимодействовать с ним через Telegram. Ниже представлены основные команды и примеры их использования:

### Команда /start

Приветственное сообщение и краткое описание бота.

![Команда /start](https://private-us-east-1.manuscdn.com/sessionFile/tJ7LhGWSh4oAEvhWe7qNd3/sandbox/Rat47Vc5e7pxtRHytzycPj-images_1749655062209_na1fn_L2hvbWUvdWJ1bnR1L1RnQm90QWRtaW5QYW5lbERlbGl2ZXJ5L2ltYWdlcy9zdGFydF9jb21tYW5k.jpg?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEo3TGhHV1NoNG9BRXZoV2U3cU5kMy9zYW5kYm94L1JhdDQ3VmM1ZTdweHRSSHl0enljUGotaW1hZ2VzXzE3NDk2NTUwNjIyMDlfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwxUm5RbTkwUVdSdGFXNVFZVzVsYkVSbGJHbDJaWEo1TDJsdFlXZGxjeTl6ZEdGeWRGOWpiMjF0WVc1ay5qcGciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3NjcyMjU2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=uIHjEQ57hiVpfaM~84nq0Q3SQWVonkBqCjxhrKgvdfVNHS1Sm1wfX51DNkJcUiZidvHcfitCDgomccv6tgk9Z4bkCMKK5vNZ1ODP8~4Pk0DQgL0B7Lzvfq8WRossjVC9gz~c3gZooAZtuwuiN0zOrnVP8nr4-JzYnn5vnwA5iWrxXSh5zbzFTubK5nDJMZe6GTCW8j731UztXEX0RmmXHJcqk8BzxWj-PGLcxstkHhWZoScpJuWVwTuoNTX0DG~Be9~aGkB~34lLRxs0LAuMVcXX6MGwcFIJiFtWTTugYQM48d5tA7b-6VGzUlGZycBkkZuQ0m9QX4D55G0TL~mpxw__)

### Список команд

Полный список доступных команд бота.

![Список команд](https://private-us-east-1.manuscdn.com/sessionFile/tJ7LhGWSh4oAEvhWe7qNd3/sandbox/Rat47Vc5e7pxtRHytzycPj-images_1749655062209_na1fn_L2hvbWUvdWJ1bnR1L1RnQm90QWRtaW5QYW5lbERlbGl2ZXJ5L2ltYWdlcy9jb21tYW5kc19saXN0.jpg?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEo3TGhHV1NoNG9BRXZoV2U3cU5kMy9zYW5kYm94L1JhdDQ3VmM1ZTdweHRSSHl0enljUGotaW1hZ2VzXzE3NDk2NTUwNjIyMDlfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwxUm5RbTkwUVdSdGFXNVFZVzVsYkVSbGJHbDJaWEo1TDJsdFlXZGxjeTlqYjIxdFlXNWtjMTlzYVhOMC5qcGciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3NjcyMjU2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=HPQ4jUJZ6FbO2qbCdpFxNkdai-UiEAs98g~t0WlfSCPAvxPi9ct0-BEijkVsBcvTR9GwDfOwSvksIxtphXkzsDe2f1MoQgbpPYJXOr-TBVdLM9ZvYHzu7U4qjP-HaSnwpJjhX6HW6kNPAES933wvQws~cUV59aRqI5QosSueM~nbxAWj1R3TIw9MOsjKoAj~7Fh~LOSU0~sE-2SfeTQx6ZS5uHMy7brBhmXrBBolP4YR3yk3RyLXRYfMyJrUSiCtjECFLWrjBpXouUA3B~~2g-~XGTq18dcTuX4Qj5xU1wbBRpx5A7ZHa7AiuSco6pPIhniYJQXF1tpno1y6mkkCdQ__)

### Работа с данными для ценообразования

Возможность изменения параметров ценообразования (стоимость доставки, курс валют, коэффициент наценки).

![Работа с данными для ценообразования](https://private-us-east-1.manuscdn.com/sessionFile/tJ7LhGWSh4oAEvhWe7qNd3/sandbox/Rat47Vc5e7pxtRHytzycPj-images_1749655062209_na1fn_L2hvbWUvdWJ1bnR1L1RnQm90QWRtaW5QYW5lbERlbGl2ZXJ5L2ltYWdlcy9wcmljZV9kYXRhX21hbmFnZW1lbnQ.jpg?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEo3TGhHV1NoNG9BRXZoV2U3cU5kMy9zYW5kYm94L1JhdDQ3VmM1ZTdweHRSSHl0enljUGotaW1hZ2VzXzE3NDk2NTUwNjIyMDlfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwxUm5RbTkwUVdSdGFXNVFZVzVsYkVSbGJHbDJaWEo1TDJsdFlXZGxjeTl3Y21salpWOWtZWFJoWDIxaGJtRm5aVzFsYm5RLmpwZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2NzIyNTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=KgJCTFgsb2OtE46LUMDSNBkIZmo~0SCuHKOb6if7QcOqpVhvvfBCUoaDUrroFRvEwf2BFRCnDPqFNG8-4S0RXKAwP13goDH364INxN2m5fjUqn25YHUNrxgy~8gqWxeQY7DLjVLhtHhtu12JLHvi6vbagUTq82QO1H-sgFsZPdRyUjSQrHyDcG-Bgxi1NMupHZL0yyPVkhZlRazrH8hgq6sjGybhYI~KLpfMlL-uCHvl72JZRTJWlJ3KK2iYP~6Gp9JeFxQ2r3VTdiRDRrRmy~z2hlVgTEN~vcJ9iJaosnZT1VMdoSkJfvq~HvJTC5sjwkjHxi1~H-9q9AqdCF4gUA__)

### Управление списком отслеживаемых товаров

Функционал для добавления и удаления товаров из отслеживания.

![Управление списком отслеживаемых товаров](https://private-us-east-1.manuscdn.com/sessionFile/tJ7LhGWSh4oAEvhWe7qNd3/sandbox/Rat47Vc5e7pxtRHytzycPj-images_1749655062209_na1fn_L2hvbWUvdWJ1bnR1L1RnQm90QWRtaW5QYW5lbERlbGl2ZXJ5L2ltYWdlcy9wcm9kdWN0X2xpc3RfbWFuYWdlbWVudA.jpg?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEo3TGhHV1NoNG9BRXZoV2U3cU5kMy9zYW5kYm94L1JhdDQ3VmM1ZTdweHRSSHl0enljUGotaW1hZ2VzXzE3NDk2NTUwNjIyMDlfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwxUm5RbTkwUVdSdGFXNVFZVzVsYkVSbGJHbDJaWEo1TDJsdFlXZGxjeTl3Y205a2RXTjBYMnhwYzNSZmJXRnVZV2RsYldWdWRBLmpwZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2NzIyNTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=LYCMdaQQJ33qVJZrEXmH~eYGCTHLYllEHnJ6z0xif62x1oBKkSmOcPbCKiX8a4Zs9QzG~JL2vw1Pkr2cRULyyBpMXwVgt1BcPJiHqrR4ZyQin3voHTZbE7509MMyf7hjetsFXF-cTr4iyfivIYAGbBdvsgSG-GSbNdvmN-zlek~B5ezsroOicsn9qiTMRMi7nO6mf6BqfCxyM0NjuvShk6Ucpy0ADEviG2rEe7S8R-9GhBR9Uaqo60~4DjqYU46dNAcw5nFQgTEfmaE9rDv3sTb6SxSYZ9dAV6LgVJ-1-L-yQ25O7JxT5Dio3uWd9cHbXGB0XvmUp3YZ5Q~uym12~g__)

*   `/add_poizon_product`: Добавить новый товар для отслеживания. Бот запросит ссылку на товар с Poizon.
*   `/delete_poizon_product`: Удалить товар из отслеживания по его номеру.
*   `/update_all_products`: Принудительное обновление всех товаров в Google Таблице.
*   `/get_data_about_price`: Показать текущие параметры ценообразования (стоимость доставки, курс, наценка).
*   `/change_data_price`: Изменить параметры ценообразования. Бот запросит новые значения в определенном формате.
*   `/get_all_poizon_products_links`: Получить список всех отслеживаемых товаров с их ссылками.
*   `/google_sheets`: Получить прямую ссылку на Google Таблицу.

## Google Таблицы

Все данные о товарах, включая их цены и другую информацию, автоматически синхронизируются с Google Таблицами, обеспечивая удобный доступ и управление данными.

![Пример Google Таблицы](https://private-us-east-1.manuscdn.com/sessionFile/tJ7LhGWSh4oAEvhWe7qNd3/sandbox/Rat47Vc5e7pxtRHytzycPj-images_1749655062210_na1fn_L2hvbWUvdWJ1bnR1L1RnQm90QWRtaW5QYW5lbERlbGl2ZXJ5L2ltYWdlcy9nb29nbGVfc2hlZXRzX2V4YW1wbGU.jpg?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEo3TGhHV1NoNG9BRXZoV2U3cU5kMy9zYW5kYm94L1JhdDQ3VmM1ZTdweHRSSHl0enljUGotaW1hZ2VzXzE3NDk2NTUwNjIyMTBfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwxUm5RbTkwUVdSdGFXNVFZVzVsYkVSbGJHbDJaWEo1TDJsdFlXZGxjeTluYjI5bmJHVmZjMmhsWlhSelgyVjRZVzF3YkdVLmpwZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2NzIyNTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=InnL~0x-LAYwP84Oo2OOcqAmiIrQYbjqoEz8hVN8D09zwjTXhihKQU~4xAaYtSe4ZnGILWYjLS6OvqTQIhqGmlInfw3c~MpOzNlpIVfyPF2i9plFZ8E-ruylt6FjNxoc2ZFkVTZRMpCQ-mP8W-mQyqxhMFcWoIDsiJTPl2TdSPQazvopJ2NYoS3zNmXg7OVaAxT0ufh2eRPFUCwE0I2AZfUsDQ8TLltl1tlPpm5CMYecLodkOSixKRQFH5XV8Lot3Axd9PeER8BxU-lEaT-qjGSutUi2PPZRaUx~B-x2hz9Qjp13R1mRjxWG8HboUJmKkyG8lZmjPjwbosPaO2jITQ__)

## Контакты

Если у вас есть вопросы или предложения, свяжитесь со мной:

*   **Telegram:** @stas_astapov
*   **GitHub:** [elmoons](https://github.com/elmoons)