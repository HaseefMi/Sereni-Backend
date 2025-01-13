from rest_framework import serializers
from .models import User, Mood, JournalEntry

class UserSerializeer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = '__all__'
class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = '__all__'