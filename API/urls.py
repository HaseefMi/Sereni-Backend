from django.urls import path
from .views import UserView, MoodView, JournalEntryView

urlpatterns = [
    path('user/', UserView.as_view(), name='user'),
    path('mood/', MoodView.as_view(), name='mood'),
    path('journal/', JournalEntryView.as_view(), name='journal')
]