from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = "user"


class DailyActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    water_intake = models.FloatField()
    sleep_hours = models.FloatField()
    meditation = models.IntegerField()


class PersonalGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_title = models.CharField(max_length=100)
    goal_description = models.TextField()
    target_date = models.DateField()
    status = models.CharField(max_length=50, choices=[
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ])

    class Meta:
        db_table = "personal_goals"


class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_date = models.DateField()
    entry_text = models.TextField()

    class Meta:
        db_table = "journal"