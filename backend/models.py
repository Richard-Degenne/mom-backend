from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=70)
    phone_number = models.CharField(max_length=15)

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    place_event = models.CharField(max_length=100)
    fk_user_created_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Network(models.Model):
    name = models.CharField(max_length=50)

class Rank(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    fk_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    # We'll need to add booleans for every single authorization

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    fk_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fk_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class TaskItem(models.Model):
    name = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    fk_task = models.ForeignKey(Task, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    fk_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    fk_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Invitation(models.Model):
    content = models.CharField(max_length=250)
    status = models.CharField(max_length=1, choices=(
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Refused'),
        ), default='P')
    date_created = models.DateTimeField(auto_now_add=True)
    fk_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fk_user_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_creator')
    fk_user_invited = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_invited')
    fk_rank = models.ForeignKey(Rank, on_delete=models.CASCADE)

class Status(models.Model):
    content = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    fk_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fk_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class IsSyncedWith(models.Model):
    user_token = models.CharField(max_length=50) # Maybe 50 is too much?
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
    fk_network = models.ForeignKey(Network, on_delete=models.CASCADE)

class IsAffectedTo(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
    fk_task = models.ForeignKey(Task, on_delete=models.CASCADE)