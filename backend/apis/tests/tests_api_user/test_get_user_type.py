from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import User, Student, Owner

class TestGetUserType(APITestCase):

    def setUp(self):

        fake = Faker('es_ES')
        self.user = Student.objects.create_user(
            dni='22334455E',
            name=fake.name(),
            surname=fake.last_name(),
            username='user1',
            password='hola1234',
            email=fake.email(), 
            telephone=fake.phone_number(),
            photo=None
        
        )

        self.user_2 = Owner.objects.create_user(
            dni='11223399P',
            name=fake.name(),
            surname=fake.last_name(),
            username='user2',
            password='hola1234',
            email=fake.email(), 
            telephone=fake.phone_number(),
            photo=None
        
        )


        self.admin = User.objects.create_superuser(
            dni='22334455A',
            name=fake.name(),
            surname=fake.last_name(),
            username='developer',
            password='developer',
            email=fake.email(), 
            telephone=fake.phone_number(),
            photo=None
        )


    
    def test_positive(self):
        response = self.client.get(f'/users/{self.user.id}/type')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['userType'], 'student')
        
        response = self.client.get(f'/users/{self.admin.id}/type')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['userType'], 'admin')

        response = self.client.get(f'/users/{self.user_2.id}/type')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['userType'], 'owner')

        response = self.client.get(f'/users/{self.user_2.id+10}/type')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['userType'], None)