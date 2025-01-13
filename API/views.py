from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import bleach
from .models import User, AccessCode, Mood, JournalEntry
from .serializers import UserSerializeer, MoodSerializer, JournalEntrySerializer
from .throttles import Throttle_100_Sec, Throttle_1_Sec
from datetime import datetime

def sanitize(data):
    sanitized_data = {}
    for key, value in data.items():
        sanitized_data[key] = bleach.clean(str(value))
    return sanitized_data
            
def save(data, action):
    sanitized_data = sanitize(data)
    if action == 'User':
        serialized_data = UserSerializeer(data=sanitized_data)
    if action == 'Mood':
        serialized_data = MoodSerializer(data=sanitized_data)
    if action == 'JournalEntry':
        serialized_data = JournalEntrySerializer(data=sanitized_data)
    if serialized_data.is_valid(raise_exception=True):
        serialized_data.save()
    return serialized_data

class UserView(APIView):
    def post(self, request, *args, **kwargs):
        code = bleach.clean(str(request.data.get('access_code')))
        if not code:
            return Response('Error: Must Provide Access Code', status=status.HTTP_401_UNAUTHORIZED)
        code_exists = AccessCode.objects.filter(code=code).exists()
        if not code_exists:
            return Response('Access Code Does Not Exist', status=status.HTTP_401_UNAUTHORIZED)
        request_data = request.data.copy()
        request_data.pop('access_code', None)  
        sanitized_data = sanitize(request_data)
        user = save(sanitized_data, 'User')
        if user:
            AccessCode.objects.filter(code=code).delete()  
        return Response(user.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        email = bleach.clean(str(request.query_params.get('email')))
        if not email:
            return Response('Error: No Email Provided', status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.filter(Q(email__icontains=email))
        if not users.exists():
            return Response('No User Found', status=status.HTTP_404_NOT_FOUND)

        user_serializer = UserSerializeer(users, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

    def get_throttles(self):
        if self.request.method == 'POST':
            return [Throttle_1_Sec()]
        return [Throttle_100_Sec()]

class MoodView(APIView):
    def post(self, request, *args, **kwargs):
        uid = bleach.clean(str(request.data.get('user_id')))
        current_date = datetime.now().date()
        prev_mood = Mood.objects.filter(date=current_date, user_id=uid).first()
        if prev_mood:
            emotion = bleach.clean(str(request.data.get('emotion')))
            if emotion:
                prev_mood.emotion = emotion
                prev_mood.save()
                serializer = MoodSerializer(prev_mood)
                return Response(serializer.data, status=status.HTTP_200_OK)
        mood = save(request.data, 'Mood')
        return Response(mood.data, status=status.HTTP_201_CREATED)
    def get(self, request, *args, **kwargs):
        uid = bleach.clean(str(request.query_params.get('uid')))
        if not uid:
            return Response('Error Must Provide a User ID', status=status.HTTP_400_BAD_REQUEST)
        moods = Mood.objects.filter(user_id=uid).order_by('-date')
        serialized_moods = MoodSerializer(moods, many=True)
        return Response(serialized_moods.data, status=status.HTTP_200_OK)
    def get_throttles(self):
        if self.request.method == 'POST':
            return [Throttle_1_Sec()]
        return [Throttle_100_Sec()]

class JournalEntryView(APIView):
    def post(self, request, *args, **kwargs):
        uid = bleach.clean(str(request.data.get('user_id')))
        current_date = datetime.now().date()
        prev_entry = JournalEntry.objects.filter(date=current_date, user_id=uid).first()
        if prev_entry:
            entry = bleach.clean(str(request.data.get('entry')))
            if entry:
                prev_entry.entry = entry
                prev_entry.save()
                serializer = JournalEntrySerializer(prev_entry)
                return Response(serializer.data, status=status.HTTP_200_OK)
        entry = save(request.data, 'JournalEntry')
        return Response(entry.data, status=status.HTTP_201_CREATED)
        
    def get(self, request, *args, **kwargs):
        uid = bleach.clean(str(request.query_params.get('uid')))
        date = request.query_params.get('date')
        
        if not uid:
            return Response('Error Must Provide a User ID', status=status.HTTP_400_BAD_REQUEST)

        if date:
            entry = JournalEntry.objects.filter(user_id=uid, date=date).first()
            if entry:
                serialized_entry = JournalEntrySerializer(entry)
                return Response(serialized_entry.data, status=status.HTTP_200_OK)
            return Response('No Entry Found for this Date', status=status.HTTP_404_NOT_FOUND)
        
        entries = JournalEntry.objects.filter(user_id=uid).order_by('-date')
        serialized_entries = JournalEntrySerializer(entries, many=True)
        return Response(serialized_entries.data, status=status.HTTP_200_OK)

    
    def get_throttles(self):
        if self.request.method == 'POST':
            return [Throttle_1_Sec()]
        return [Throttle_100_Sec()]