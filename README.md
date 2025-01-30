# WhatsApp Reminder Bot

## Описание проекта

Проект представляет собой систему напоминаний, которая использует Celery для асинхронной обработки задач и отправки сообщений в WhatsApp через GreenAPI. Каждый пользователь может добавить напоминание с указанием времени и текста. Также предусмотрены команды для отображения текущих напоминаний и их удаления.
Напоминания могут повторяться через день, неделю или месяц, в зависимости от настроек пользователя.
Процесс работы бота автоматизирован, и напоминания отправляются пользователям в установленное время. Для этого используется асинхронная обработка с помощью Celery.

## Используемые технологии

- **Django REST Framework (DRF)** — для создания API.
- **Celery** — асинхронная обработка задач.
- **Redis** — брокер сообщений для Celery.
- **GreenAPI** — интеграция с WhatsApp для отправки сообщений.
- **SQLite** — база данных для хранения напоминаний.
- **Flower** — для мониторинга.  

## Установка и запуск

### 1. Клонирование репозитория  

```bash
git clone https://github.com/DzusDaTo/WhatsApp_Bot.git
cd whatsapp_bot
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Применение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Запуск серверов

```bash
redis-server
celery -A whatsapp_bot worker --loglevel=info
celery -A whatsapp_bot beat --loglevel=info
python manage.py runserver
```

## Использование API

- Добавить напоминание: `POST /reminders/`  
- Просмотреть напоминания: `GET /reminders/`  
- Удалить напоминание: `DELETE /reminders/{id}/`

