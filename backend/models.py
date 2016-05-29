from django.db import models

# Create your models here.

class User(models.Model):
    """
    A User is an entity (a person), who has an account on Mom.
    """
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=70, null=False, unique=True, blank=False)
    phone_number = models.CharField(max_length=15, null=True, unique=True)

    def json_detail(self):
        """
        Gives a dictionnary containing the main information about a User.

        @ return A dictionnary in the following format:
        `{'pk':pk, 'first_name':first_name, 'last_name':last_name, 'email':email,
        'phone_number':phone_number}`
        """
        return {
                'pk': self.pk,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'email': self.email,
                'phone_number': self.phone_number
        }

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    place_event = models.CharField(max_length=100)
    fk_user_created_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def json_detail(self):
        """
        Gives a dictionnary containing the main information about an Event.

        @ return A dictionnary in the following format:
        `{'pk':pk, 'name':name, 'description':description, 'date':date,
        'place_event':place_event, 'date_created': date_created,
        'pk_user_created': fk_user_created_by}`
        """
        return {
                'pk': self.pk,
                'name': self.name,
                'description': self.description,
                'date': self.date,
                'place_event': self.place_event,
                'date_created': self.date_created,
                'pk_user_created_by': self.fk_user_created_by.pk
        }

class Network(models.Model):
    name = models.CharField(max_length=50)

class Rank(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    is_attendee = models.BooleanField(null=False, default=True)
    is_organiser = models.BooleanField(null=False, default=False)
    is_admin = models.BooleanField(null=False, default=False)
    fk_event = models.ForeignKey(Event, on_delete=models.CASCADE)

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    fk_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    fk_user_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def json_detail(self):
        return {'pk': self.pk,
                'name': self.name,
                'description': self.description,
                'date_created': self.date_created,
                'pk_event': self.fk_event.pk,
                'pk_user_created_by': self.fk_user_created_by.pk
        }

class TaskItem(models.Model):
    name = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    fk_task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def json_detail(self):
        return {'pk': self.pk,
                'name': self.name,
                'completed': self.completed,
                'date_created': self.date_created,
                'pk_task': self.fk_task.pk
        }

class Comment(models.Model):
    content = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    fk_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    fk_user_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def json_detail(self):
        return {'pk': self.pk,
                'content': self.content,
                'date_created': self.date_created,
                'pk_task': self.fk_task.pk,
                'pk_user_created_by': self.fk_user_created_by.pk
        }

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
    fk_user_created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def json_detail(self):
        return {'pk': self.pk,
                'content': self.content,
                'date_created': self.date_created,
                'pk_event': self.fk_event.pk,
                'pk_user_created_by': self.fk_user.pk
        }

class IsSyncedWith(models.Model):
    user_token = models.CharField(max_length=50) # Maybe 50 is too much?
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
    fk_network = models.ForeignKey(Network, on_delete=models.CASCADE)

class IsAffectedTo(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
    fk_task = models.ForeignKey(Task, on_delete=models.CASCADE)
