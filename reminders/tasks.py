from celery import shared_task
from .models import Reminder
import requests
from datetime import datetime, timedelta
import pytz


@shared_task
def send_whatsapp_message_task(reminder_id):
    """
    Задача Celery для отправки сообщения через GreenAPI.
    """
    try:
        reminder = Reminder.objects.get(id=reminder_id)
        phone_number = reminder.phone_number
        message = reminder.message

        url = 'https://api.green-api.com/sendMessage'
        data = {
            'phone': phone_number,
            'message': message,
            'token': 'b96b4c88d9634ef08247566349fd450bbb11d2b6b10944b0b7',
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            print(f"Сообщение отправлено на {phone_number}")
        else:
            print(f"Ошибка при отправке сообщения: {response.text}")

    except Reminder.DoesNotExist:
        print("Напоминание не найдено")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


@shared_task
def check_reminders():
    """
    Задача для проверки напоминаний каждую минуту и отправки сообщений.
    """
    now = datetime.now(pytz.UTC)
    reminders = Reminder.objects.filter(send_time__lte=now, sent=False)

    for reminder in reminders:
        send_whatsapp_message_task.apply_async(args=[reminder.id])
        reminder.sent = True
        reminder.save()

        # Обработка повторяющихся напоминаний
        if reminder.repeat:
            next_send_time = get_next_send_time(reminder)
            if next_send_time:
                reminder.send_time = next_send_time
                reminder.sent = False  # Сбрасываем статус, чтобы оно отправилось снова
                reminder.save()


def get_next_send_time(reminder):
    """
    Функция для вычисления следующего времени отправки для повторяющихся напоминаний.
    """
    if reminder.repeat == Reminder.DAILY:
        return reminder.send_time + timedelta(days=1)
    elif reminder.repeat == Reminder.WEEKLY:
        return reminder.send_time + timedelta(weeks=1)
    elif reminder.repeat == Reminder.MONTHLY:
        return reminder.send_time + timedelta(weeks=4)  # Приблизительное значение для ежемесячных
    return None
