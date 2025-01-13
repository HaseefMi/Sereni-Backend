from django.contrib import admin
from .models import User, Mood, AccessCode, JournalEntry

admin.site.register(User)
admin.site.register(Mood)
admin.site.register(AccessCode)
admin.site.register(JournalEntry)