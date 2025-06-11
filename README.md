# Telegram Bot Admin Panel for Poizon Price Tracking




## Описание Проекта

Этот Telegram-бот представляет собой административную панель для отслеживания цен на товары с платформы Poizon. Он позволяет администраторам добавлять и удалять товары, а также автоматически обновлять их цены и сохранять данные в Google Таблицах. Проект разработан с использованием современных технологий и обеспечивает удобное управление данными о товарах.

## Ключевые Особенности

*   **Добавление товаров:** Легкое добавление новых товаров с Poizon по ссылке.
*   **Удаление товаров:** Возможность удаления товаров из отслеживания.
*   **Автоматическое обновление цен:** Цены на товары автоматически обновляются в фоновом режиме.
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

![Команда /start](https://private-us-east-1.manuscdn.com/sessionFile/tJ7LhGWSh4oAEvhWe7qNd3/sandbox/NIuo9JH2NbVwDgczGqUOxN-images_1749654115495_na1fn_L2hvbWUvdWJ1bnR1L1RnQm90QWRtaW5QYW5lbERlbGl2ZXJ5L2ltYWdlcy9zdGFydF9jb21tYW5k.jpg?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEo3TGhHV1NoNG9BRXZoV2U3cU5kMy9zYW5kYm94L05JdW85SkgyTmJWd0RnY3pHcVVPeE4taW1hZ2VzXzE3NDk2NTQxMTU0OTVfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwxUm5RbTkwUVdSdGFXNVFZVzVsYkVSbGJHbDJaWEo1TDJsdFlXZGxjeTl6ZEdGeWRGOWpiMjF0WVc1ay5qcGciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3NjcyMjU2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=Sp-G7K~drJHwuvvNjrdUPWs~jIvWEBHaDFG1chwH345tZAzAXgoQeAe2WFTPNS0pXuhMl1cJhpax37u672bxwsocD4o3c175FqEqTukVEkYHjXGQbkA8lZabSLh0sETJOXCNv~lq57n3prWMh7o9biM0yH3UL9LBY0J-PMjVwYZVEi6MDAKWNCIhUCXkfrD7jfLOkKriXykd4F~tN6gFm~9lnkvMKIe5FiHW9P6QCHsJ6F2JmQqIUieCwbkOjdMZ2YW8ms7h3ciHKIE4A02TOJpem2O80kRpOOn3Kh2EeqtRGJi4xGFgzoonCaOCZglJrVnCgk-qY0Hh8xmbkEfOdw__)

### Список команд

Полный список доступных команд бота.

![Список команд](https://private-us-east-1.manuscdn.com/sessionFile/tJ7LhGWSh4oAEvhWe7qNd3/sandbox/NIuo9JH2NbVwDgczGqUOxN-images_1749654115495_na1fn_L2hvbWUvdWJ1bnR1L1RnQm90QWRtaW5QYW5lbERlbGl2ZXJ5L2ltYWdlcy9jb21tYW5kc19saXN0.jpg?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEo3TGhHV1NoNG9BRXZoV2U3cU5kMy9zYW5kYm94L05JdW85SkgyTmJWd0RnY3pHcVVPeE4taW1hZ2VzXzE3NDk2NTQxMTU0OTVfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwxUm5RbTkwUVdSdGFXNVFZVzVsYkVSbGJHbDJaWEo1TDJsdFlXZGxjeTlqYjIxdFlXNWtjMTlzYVhOMC5qcGciLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3NjcyMjU2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=G4QoPxGrw33K8wRxrz7m230McoiHt8c6vpFb3j5TAsf3NCAKzCdR3BDkX510or-z0lttR96DqNPknWsUnOfuLfYKmRRxFpkc0cg5dJJtq7XAVphg5vosFAw9~csdrSDI9LDZSPP1jQV8As9hbb2AwOJ-QtCkgvEsHNRpE5Zk8QreNiaogjIFH0yC0FGMCMGJvw9m9bdOWqyTxKj37pUtY99~ZsVf6Pgxt9HpvGqFvbD0RPP2~kwqW7mtd7x0ivE0vCV~yvGJpB46Ar6AbAdymQYVdufk6nU3wtx4pqXaKxFvtmh4fPi9Roo0s3wBteYnAB2Otn86tgOl~BwexTT10w__)

### Работа с данными для ценообразования

Возможность изменения параметров ценообразования (стоимость доставки, курс валют, коэффициент наценки).

![Работа с данными для ценообразования](https://private-us-east-1.manuscdn.com/sessionFile/tJ7LhGWSh4oAEvhWe7qNd3/sandbox/NIuo9JH2NbVwDgczGqUOxN-images_1749654115495_na1fn_L2hvbWUvdWJ1bnR1L1RnQm90QWRtaW5QYW5lbERlbGl2ZXJ5L2ltYWdlcy9wcmljZV9kYXRhX21hbmFnZW1lbnQ.jpg?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEo3TGhHV1NoNG9BRXZoV2U3cU5kMy9zYW5kYm94L05JdW85SkgyTmJWd0RnY3pHcVVPeE4taW1hZ2VzXzE3NDk2NTQxMTU0OTVfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwxUm5RbTkwUVdSdGFXNVFZVzVsYkVSbGJHbDJaWEo1TDJsdFlXZGxjeTl3Y21salpWOWtZWFJoWDIxaGJtRm5aVzFsYm5RLmpwZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2NzIyNTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=Oocjdkry862wDPpPkA2V0D33Wu1XMTr6Jq4fxmnaY8Rkgm3SZ81GI6vCmNI7CpjLS0WHiFnMx80KHKl8qTvq5j9ONEuRvuxsA0UizP988Dp7gIEBaz4~GY2TqlPJc4-2bR3BJ2ak~RIKTkFRjPtZBLD3UBX4thfRISK0g98JWVyj-UZDJXMqJublhlpF~ZJaywixc-16gRQInZYU1yv0LFsqiBVow92DbZkEiFT9M0JDuWEJwxSHCkShDvYWT58x1pqPd7gTi6L4VqspHiwTOZ8tX3UNPoGnVouw9PTUvq5qN2Cq9D~ineke2Oh9~yHEiX0CyB8ycPrQb~tKFHlzkg__)

### Управление списком отслеживаемых товаров

Функционал для добавления и удаления товаров из отслеживания.

![Управление списком отслеживаемых товаров](https://private-us-east-1.manuscdn.com/sessionFile/tJ7LhGWSh4oAEvhWe7qNd3/sandbox/NIuo9JH2NbVwDgczGqUOxN-images_1749654115495_na1fn_L2hvbWUvdWJ1bnR1L1RnQm90QWRtaW5QYW5lbERlbGl2ZXJ5L2ltYWdlcy9wcm9kdWN0X2xpc3RfbWFuYWdlbWVudA.jpg?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvdEo3TGhHV1NoNG9BRXZoV2U3cU5kMy9zYW5kYm94L05JdW85SkgyTmJWd0RnY3pHcVVPeE4taW1hZ2VzXzE3NDk2NTQxMTU0OTVfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwxUm5RbTkwUVdSdGFXNVFZVzVsYkVSbGJHbDJaWEo1TDJsdFlXZGxjeTl3Y205a2RXTjBYMnhwYzNSZmJXRnVZV2RsYldWdWRBLmpwZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc2NzIyNTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=ByF-fjNGQR05D0IZpOkbAg75mkb-L3jukDcOEFkqotvK~xZZssibEx70AiykIjpBXwLAPhMPvh4rQI0gIQIWqE6cWnZlR6hzSxTCB6fi1sWABgRzQ-oCRCMvVFz2H13vqJavK2Bea~xxW7U5mlNSxZeMJZwiy4UIwQYRtnfqXjnnBygdxTb9y2dzNiRINoqQn8UeSDfV1ttlBzi~glMbnuw8qZY0FpVpGnjVNChF-r21o9tGwI-o1Z6iEuWu9X5Ys0KkDcvuO1S3o461OCdw8fBqgKmAdIxVy8dIwQp-TOWE4z9eH6yqzLptUA9PxLUlzPIBQMzsUfJltRVlO1VrFQ__)

*   `/add_poizon_product`: Добавить новый товар для отслеживания. Бот запросит ссылку на товар с Poizon.
*   `/delete_poizon_product`: Удалить товар из отслеживания по его номеру.
*   `/update_all_products`: Принудительное обновление всех товаров в Google Таблице.
*   `/get_data_about_price`: Показать текущие параметры ценообразования (стоимость доставки, курс, наценка).
*   `/change_data_price`: Изменить параметры ценообразования. Бот запросит новые значения в определенном формате.
*   `/get_all_poizon_products_links`: Получить список всех отслеживаемых товаров с их ссылками.
*   `/google_sheets`: Получить прямую ссылку на Google Таблицу.


## Контакты

Если у вас есть вопросы или предложения, свяжитесь со мной:

*   **Telegram:** @elmoons
*   **GitHub:** [elmoons](https://github.com/elmoons)


