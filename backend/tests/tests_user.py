import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from backend.models import *

# Create your tests here.

####################
# HELPER FUNCTIONS #
####################


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
    def sign_in(self):
        """
        Log in as a test user to authenticate for further testing.
        """
        u = User.objects.create(first_name = "Testing",
                last_name = 'Tester',
                password='******',
                email='testing.tester@mom.com',
                phone_number='000-000-0000')
        self.client.session['pk_user'] = u.pk

    def test_unknown_user(self):
        """
        A query for an unknown user must return a 404 status code.
        """
        self.sign_in()
        response = self.client.get(reverse('backend:user_details', args=(0,)))
        self.assertEqual(response.status_code, 404)

    def test_known_user(self):
        """
        A query for a known user must return a JSON object containing
        the user's informations.
        """
        self.sign_in()
        u = User.objects.create(first_name = "David",
                last_name = 'Smith',
                password='******',
                email='david.smith@mom.com',
                phone_number='012-345-6789')
        response = self.client.get(reverse('backend:user_details', args=(u.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), u.json_detail())

class UserEventsTests(TestCase):
    def sign_in(self):
        """
        Log in as a test user to authenticate for further testing.
        """
        u = User.objects.create(first_name = "Testing",
                last_name = 'Tester',
                password='******',
                email='testing.tester@mom.com',
                phone_number='000-000-0000')
        self.client.session['pk_user'] = u.pk

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
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
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
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
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
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
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
        self.assertDictContainsSubset({'message': "Missing parameters"}, response.json())

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
        self.assertDictContainsSubset({'message': "Password/Email cannot be empty"}, response.json())

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
        self.assertDictContainsSubset({'message': "Missing parameters"}, response.json())

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
        self.assertDictContainsSubset({'message': "Password/Email cannot be empty"}, response.json())

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
        self.assertDictContainsSubset({'message': "Phone number/email already exists"}, response.json())

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
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
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
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
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
        self.assertDictContainsSubset({'message': "Phone number/email already exists"}, response.json())

class UserSignInTests(TestCase):
    def test_sign_in(self):
        """
        Sending a correct sign in request must return a JSON object with the
        correct values.
        """
        user = User.objects.create(email='david.smith@mom.com', password='******')
        response = self.client.post(reverse('backend:sign_in'), {'email':user.email, 'password':user.password})
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset({'status': 'success'}, response.json())
        self.assertDictContainsSubset({'pk_user': user.pk}, response.json())

    def test_sign_in_no_email(self):
        """
        Sending a sign in request without an `email` request parameter must return
        a 400 error.
        """
        response = self.client.post(reverse('backend:sign_in'), {'password': '******'})
        self.assertEqual(response.status_code, 400)
        self.assertDictContainsSubset({'status': "failure"}, response.json())
        self.assertDictContainsSubset({'message': "Missing parameters"}, response.json())

    def test_sign_in_no_password(self):
        """
        Sending a sign in request without a `password` request parameter must return
        a 400 error.
        """
        response = self.client.post(reverse('backend:sign_in'), {'email': 'david.smith@mom.com'})
        self.assertEqual(response.status_code, 400)
        self.assertDictContainsSubset({'status': "failure"}, response.json())
        self.assertDictContainsSubset({'message': "Missing parameters"}, response.json())

    def test_sign_in_invalid_email(self):
        """
        Sending a sign in request with an invalid `email` request parameter must
        return a 401 error.
        """
        user = User.objects.create(email='david.smith@mom.com', password='******')
        response = self.client.post(reverse('backend:sign_in'), {'email': 'wrong@email.com', 'password': user.password})
        self.assertEqual(response.status_code, 401)
        self.assertDictContainsSubset({'status': "failure"}, response.json())
        self.assertDictContainsSubset({'message': "Incorrect email/password"}, response.json())

    def test_sign_in_invalid_password(self):
        """
        Sending a sign in request with an invalid `email` request parameter must
        return a 401 error.
        """
        user = User.objects.create(email='david.smith@mom.com', password='******')
        response = self.client.post(reverse('backend:sign_in'), {'email': user.email, 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 401)
        self.assertDictContainsSubset({'status': "failure"}, response.json())
        self.assertDictContainsSubset({'message': "Incorrect email/password"}, response.json())

