from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Reminder
from .serializers import ReminderSerializer
from datetime import datetime
import pytz


class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Получить список будущих напоминаний"""
        now = datetime.now(pytz.UTC)
        reminders = Reminder.objects.filter(send_time__gt=now)
        serializer = self.get_serializer(reminders, many=True)
        return Response(serializer.data)

