<div align="center">

<img src="app/static/img/logo.png" alt="CKPcoin" width="120">

# CKPcoin

**Telegram Mini App с внутренней «криптой» колледжа: токены за активность, рейтинг и награды**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-migrations-6BA81E?style=for-the-badge)

</div>

---

## 📖 О проекте

CKPcoin — проект студентов, в котором внутренняя валюта (токены **CKP**) начисляется за участие в мероприятиях и активностях. Студент регистрируется в Telegram-боте по секретному ключу и дальше работает в Mini App: смотрит баланс, профиль, список мероприятий и рейтинг лидеров. Кураторы начисляют награды участникам мероприятий прямо из веб-интерфейса.

## ✨ Возможности

- 🤖 **Telegram-бот** (aiogram 3, режим webhook): регистрация пользователя по секретному ключу, уведомления администраторов о запуске и остановке бота
- 📱 **Mini App** на Jinja2-шаблонах: главная с балансом, профиль, кошелёк, портфолио мероприятий, топ пользователей
- 🏆 **Рейтинг** — топ-10 пользователей по балансу
- 🎟 **Мероприятия** — активные и прошедшие, у каждого своя награда (`award`) и список участников
- 💰 **Начисление наград** — выбор участников мероприятия и массовое начисление токенов с добавлением события в портфолио
- 👥 **Группы и роли** пользователей (модели `Group`, `Role`)
- 📝 **JSON-логирование** запросов с временем обработки

## 🧱 Стек

| Технология | Роль |
|---|---|
| FastAPI + Uvicorn | REST API, отдача страниц и статики |
| aiogram 3 | Telegram-бот, приём обновлений через `/webhook` |
| SQLAlchemy 2 (async) + aiosqlite | ORM и доступ к БД (URL берётся из `DB_URL`) |
| Alembic | миграции (`app/migration`) |
| Pydantic Settings | конфигурация из `.env` |
| Jinja2 + HTML/CSS/JS | страницы Mini App (Telegram WebApp SDK) |

## 🗂 Структура проекта

```text
app/
├── main.py            # FastAPI-приложение, lifespan, webhook бота
├── config.py          # настройки из .env
├── database.py        # async-движок, сессии, базовая модель
├── bot/               # создание бота и обработчики (/start, ввод ключа)
├── users/             # модели User/Group/Role, DAO, роутер, регистрация
├── events/            # мероприятия и участники
├── pages/             # HTML-страницы Mini App
├── dao/base.py        # базовый DAO
├── migration/         # окружение Alembic
├── templates/         # Jinja2-шаблоны
└── static/            # css, js, иконки, изображения, pres.pdf
data/crate_random_user.py  # скрипт генерации тестовых пользователей
```

## 🚀 Быстрый старт

```bash
git clone https://github.com/Edvvard0/CKRcoin.git
cd CKRcoin

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install python-json-logger     # импортируется в app/logger.py, в requirements.txt его нет

# создайте .env в корне проекта (имена переменных — в разделе ниже)

alembic upgrade head               # применить миграции
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

> Бот работает через webhook: `BASE_SITE` должен быть публичным HTTPS-адресом приложения — на него регистрируется `{BASE_SITE}/webhook`.

## ⚙️ Конфигурация

Переменные читаются из файла `.env` в корне проекта (`app/config.py`).

| Переменная | Назначение |
|---|---|
| `BOT_TOKEN` | токен Telegram-бота |
| `ADMIN_IDS` | список Telegram ID администраторов (получают уведомления о старте/остановке) |
| `BASE_SITE` | публичный URL приложения, используется для webhook |
| `DB_URL` | URL основной БД (async SQLAlchemy) |
| `TEST_DB_URL` | URL тестовой БД (используется при `MODE=TEST`) |
| `MODE` | режим: `TEST` / `DEV` / `PROD` |
| `API_HOST`, `API_PORT` | хост и порт Uvicorn |
| `LOG_LEVEL` | уровень логирования |

## 🔌 API / Команды

**Команда бота:** `/start` — проверка регистрации; любое следующее текстовое сообщение трактуется как секретный ключ для привязки Telegram-аккаунта.

<details>
<summary>HTTP-эндпоинты</summary>

| Метод | Путь | Описание |
|---|---|---|
| POST | `/webhook` | приём обновлений Telegram |
| GET | `/event/all_events`, `/event/all_active_events`, `/event/all_past_events` | списки мероприятий |
| GET | `/event/event_by_id/{event_id}` | мероприятие по id |
| GET | `/event/event_participant?event_id=` | участники мероприятия |
| GET | `/users/`, `/users/profile/{tg_id}`, `/users/top_10` | пользователи, профиль, топ-10 |
| GET | `/users/users_my_group`, `/users/portfolio/{tg_id}` | пользователи группы, портфолио |
| POST | `/users/award_users` | начислить награду пользователям |
| POST | `/users/events/{event_id}/participants` | добавить участников в мероприятие |
| POST | `/users/events/{event_id}/award_and_add` | начислить награду и добавить мероприятие в портфолио |
| POST / PATCH / DELETE | `/users/add_user`, `/users/update_user/{tg_id}`, `/users/delete_user/{tg_id}` | управление пользователями |
| GET | `/pages/...` | HTML-страницы Mini App (main, profile, wallet, top_users, all_events и др.) |

Интерактивная документация — `/docs` (Swagger UI, штатная для FastAPI).

</details>

## 🗺 Планы

В Mini App есть ссылка «Дорожная карта» — презентация лежит в [`app/static/img/pres.pdf`](app/static/img/pres.pdf).

<!-- TODO: скриншот -->

## 👤 Автор

**Эдвард Осипчук** · GitHub [@Edvvard0](https://github.com/Edvvard0) · Telegram [@Edward0076](https://t.me/Edward0076)
