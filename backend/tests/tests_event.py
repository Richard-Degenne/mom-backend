import json
from datetime import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone

from backend.models import *

# Create your tests here.

####################
# HELPER FUNCTIONS #
####################


class EventMethodsTests(TestCase):
    def test_json_detail(self):
        """
        The @ref Event.json_detail method should return a dictionnary in the
        adequate format.
        """
        u = User.objects.create(first_name = "David",
                last_name = 'Smith',
                password='******',
                email='david.smith@mom.com',
                phone_number='012-345-6789')
        e = Event(name = "Birthday party",
                description = "Come to celebrate David Smith's birthday!",
                date = datetime.now()+timezone.timedelta(days=1),
                place_event = "David's place",
                date_created = datetime.now(),
                fk_user_created_by = u.pk)
        self.assertDictEqual(u.json_detail(), {'pk':None,
                name: "Birthday party",
                description: "Come to celebrate David Smith's birthday!",
                date: datetime.now()+timezone.timedelta(days=1),
                place_event: "David's place",
                date_created: datetime.now(),
                fk_user_created_by: u.pk})

class EventDetailsTests(TestCase):
    def sign_in(self):
        """
        Log in as a test user to authenticate for further testing.
        """
        u = User.objects.create(first_name = "Testing",
                last_name = 'Tester',
                password='******',
                email='testing.tester@mom.com',
                phone_number='000-000-0000')
        self.client.session['user_pk'] = u.pk

class EventCreateTests(TestCase):
    def sign_in(self):
        """
        Log in as a test user to authenticate for further testing.
        """
        u = User.objects.create(first_name = "Testing",
                last_name = 'Tester',
                password='******',
                email='testing.tester@mom.com',
                phone_number='000-000-0000')
        self.client.session['user_pk'] = u.pk

