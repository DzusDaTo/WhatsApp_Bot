from django.db import models


class Reminder(models.Model):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

    REPEAT_CHOICES = [
        (DAILY, 'Ежедневно'),
        (WEEKLY, 'Еженедельно'),
        (MONTHLY, 'Ежемесячно'),
    ]
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    message = models.TextField(verbose_name='Сообщение')
    send_time = models.DateTimeField(verbose_name='Время отправки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')
    repeat = models.CharField(max_length=10, choices=REPEAT_CHOICES, null=True, blank=True)
    sent = models.BooleanField(default=False, verbose_name='Отправлено')

    def __str__(self):
        return f"Напоминание для {self.phone_number} на {self.send_time}"

    class Meta:
        verbose_name = 'Напоминание'
        verbose_name_plural = 'Напоминания'

