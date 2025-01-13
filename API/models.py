from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    def __str__(self):
        return self.name
class AccessCode(models.Model):
    code = models.CharField(max_length=255)
    def __str__(self):
        return self.code

class Mood(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    emotion = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.user_id} - {self.date} - {self.emotion}"
class JournalEntry(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    entry = models.TextField()
    def __str__(self):
        return f"{self.user_id} - {self.date} - {self.entry}"