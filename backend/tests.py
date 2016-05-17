import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import *

# Create your tests here.

class UserMethodsTests(TestCase):
    def test_json_detail(self):
        """
        The @ref User.json_detail method should return a dictionnary in the
        adequate format.
        """
        u = User(first_name = "David",
                last_name = 'Smith',
                password='******',
                email='david.smith@mom.com',
                phone_number='012-345-6789')
        self.assertDictEqual(u.json_detail(), {'pk':None,
                'first_name': "David",
                'last_name': 'Smith',
                'email': 'david.smith@mom.com',
                'phone_number': '012-345-6789'})

class UserDetailsTests(TestCase):
    def test_unknown_user(self):
        """
        A query for an unknown user must return a 404 status code.
        """
        response = self.client.get(reverse('backend:user_details', args=(1,)))
        self.assertEqual(response.status_code, 404)

    def test_known_user(self):
        """
        A query for a known user must return a JSON object containing
        the user's informations.
        """
        u = User.objects.create(first_name = "David",
                last_name = 'Smith',
                password='******',
                email='david.smith@mom.com',
                phone_number='012-345-6789')
        response = self.client.get(reverse('backend:user_details', args=(u.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), u.json_detail())

class UserRegisterTests(TestCase):
    def register(self, params):
        return self.client.post(reverse('backend:user_register'), params)

    def test_register(self):
        """
        Sending a valid register request must return the newly_created user.
        """
        u = User(first_name = "David",
                last_name = 'Smith',
                password='******',
                email='david.smith@mom.com',
                phone_number='012-345-6789')
        response = self.register({
                'first_name': u.first_name,
                'last_name': u.last_name,
                'password': u.password,
                'email': u.email,
                'phone_number': u.phone_number
        })
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), self.client.get(reverse('backend:user_details', args=(response.json()['pk'],))).json())

    def test_no_first_name(self):
        """
        Sending a request without a `first_name` request parameter must return
        a User with an empty string as a first name.
        """
        response = self.register({
                'last_name': "Smith",
                'password': '******',
                'email': "david.smith@mom.com",
                'phone_number': "012-345-6789"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['first_name'], '')

    def test_no_last_name(self):
        """
        Sending a request without a `last_name` request parameter must return
        a User with an empty string as a last name.
        """
        response = self.register({
                'first_name': "David",
                'password': '******',
                'email': "david.smith@mom.com",
                'phone_number': "012-345-6789"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['last_name'], '')

    def test_no_password(self):
        """
        Sending a request without a `password` request parameter must return
        a 400 error.
        """
        response = self.register({
                'first_name': "David",
                'last_name': "Smith",
                'email': "david.smith@mom.com",
                'phone_number': "012-345-6789"
        })
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'message': "Missing parameters"})

    def test_blank_password(self):
        """
        Sending a request wit a blank `password` request parameter must return
        a 400 error.
        """
        response = self.register({
                'first_name': "David",
                'last_name': "Smith",
                'password': '',
                'email': "david.smith@mom.com",
                'phone_number': "012-345-6789"
        })
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'message': "Password/Email cannot be empty"})

    def test_no_email(self):
        """
        Sending a request without an `email` request parameter must return
        a 400 error.
        """
        response = self.register({
                'first_name': "David",
                'last_name': "Smith",
                'password': "******",
                'phone_number': "012-345-6789"
        })
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'message': "Missing parameters"})

    def test_blank_email(self):
        """
        Sending a request with a blank `email` request parameter must return
        a 400 error.
        """
        response = self.register({
                'first_name': "David",
                'last_name': "Smith",
                'password': '******',
                'email': "",
                'phone_number': "012-345-6789"
        })
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'message': "Password/Email cannot be empty"})

    def test_duplicate_email(self):
        """
        Sending a request with an already existing `email` request parameter must return
        a 400 error.
        """
        params = {
                'first_name': "David",
                'last_name': "Smith",
                'password': '******',
                'email': "david.smith@mom.com",
                'phone_number': "012-345-6789"
        }
        self.register(params)
        response = self.register(params)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'message': "Phone number/email already exists"})

    def test_no_phone_number(self):
        """
        Sending a request without an `phone_number` request parameter must return
        a User with None as a phone number.
        """
        response = self.register({
                'first_name': "David",
                'last_name': "Smith",
                'password': "******",
                'email': "david.smith@mom.com",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['phone_number'], None)

    def test_blank_phone_number(self):
        """
        Sending a request with a blank `phone_number` request parameter must return
        a User with None as a phone number.
        """
        response = self.register({
                'first_name': "David",
                'last_name': "Smith",
                'password': '******',
                'email': "david.smith@mom.com",
                'phone_number': ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['phone_number'], None)

    def test_duplicate_phone_number(self):
        """
        Sending a request with an already existing `phone_number` request parameter must return
        a 400 error.
        """
        params = {
                'first_name': "David",
                'last_name': "Smith",
                'password': '******',
                'email': "david.smith@mom.com",
                'phone_number': "012-345-6789"
        }
        self.register(params)
        response = self.register(params)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {'message': "Phone number/email already exists"})
