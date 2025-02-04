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


class PersonalGoals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    goal_title = models.CharField(max_length=100)  # Title of the goal
    goal_description = models.TextField()  # Details about the goal
    target_date = models.DateField()  # Deadline for achieving the goal
    status = models.CharField(max_length=50, choices=[
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ])  # Status of the goal

    class Meta:
        db_table = "personal_goals"


class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    entry_date = models.DateField()  # Date of the journal entry
    entry_text = models.TextField()  # Content of the journal

    class Meta:
        db_table = "journal"