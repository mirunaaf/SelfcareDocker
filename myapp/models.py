from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = "user"


class DailyActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    date = models.DateField()
    water_intake = models.FloatField()
    sleep_hours = models.FloatField()
    meditation = models.IntegerField()