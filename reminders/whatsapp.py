import requests
from .models import Reminder
import pytz
from datetime import datetime
import time


def send_whatsapp_message(phone_number, message):
    """
    Отправляет сообщение через GreenAPI.
    """
    url = 'https://api.green-api.com/sendMessage'
    data = {
        'phone': phone_number,
        'message': message,
        'token': 'c2e558903ae54d5f93da291d7b8cc5fbb4cfcf3c2d2a44e8b5',
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"Сообщение отправлено на {phone_number}")
    else:
        print(f"Ошибка при отправке сообщения: {response.text}")


def check_reminders():
    """
    Проверяет напоминания каждую минуту и отправляет задачи через Celery.
    """
    from .tasks import send_whatsapp_message_task

    while True:
        now = datetime.now(pytz.UTC)
        reminders = Reminder.objects.filter(send_time__lte=now)
        for reminder in reminders:
            send_whatsapp_message_task.apply_async(args=[reminder.id])
        time.sleep(60)


def add_reminder(update, context):
    """Команда для добавления напоминания с временем и сообщением."""
    try:
        time_str = context.args[0]
        message = ' '.join(context.args[1:-1])
        repeat = context.args[-1] if len(context.args) > 2 else None  # Повторение

        time_format = '%d.%m.%Y %H:%M'
        send_time = datetime.strptime(time_str, time_format)

        send_time = pytz.utc.localize(send_time)

        reminder = Reminder.objects.create(
            message=message,
            send_time=send_time,
            phone_number=update.message.chat_id,
            repeat=repeat if repeat in [Reminder.DAILY, Reminder.WEEKLY, Reminder.MONTHLY] else None
        )

        update.message.reply_text(f"Напоминание установлено: {message} на {send_time.strftime(time_format)}")

    except IndexError:
        update.message.reply_text("Пожалуйста, укажите время и сообщение.")
    except ValueError:
        update.message.reply_text("Неверный формат времени. Используйте формат: ДД.ММ.ГГГГ ЧЧ:ММ.")


def show_reminders(update, context):
    """Команда для отображения текущих напоминаний."""
    reminders = Reminder.objects.filter(sent=False)
    message = "Текущие напоминания:\n"
    for reminder in reminders:
        message += f"{reminder.message} для {reminder.phone_number} в {reminder.send_time} (Повтор: {reminder.repeat()})\n"
    update.message.reply_text(message)


def delete_reminder(update, context):
    """Команда для удаления напоминания по ID."""
    try:
        reminder_id = int(context.args[0])
        reminder = Reminder.objects.get(id=reminder_id)
        reminder.delete()
        update.message.reply_text(f"Напоминание с ID {reminder_id} было удалено.")
    except (IndexError, ValueError):
        update.message.reply_text("Пожалуйста, укажите корректный ID напоминания.")
    except Reminder.DoesNotExist:
        update.message.reply_text("Напоминание с таким ID не найдено.")