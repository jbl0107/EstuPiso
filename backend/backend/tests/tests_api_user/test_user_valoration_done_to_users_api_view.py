from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import User, UserValoration

class TestUserDetailApiView(APITestCase):

    
    def setUp(self):

        fake = Faker('es_ES')
        self.user = User.objects.create_user(
            dni='22334455E',
            name=fake.name(),
            surname=fake.last_name(),
            username='user1',
            password='hola1234',
            email=fake.email(), 
            telephone=fake.phone_number(),
            photo=None
        
        )

        self.user_2 = User.objects.create_user(
            dni='11223399P',
            name=fake.name(),
            surname=fake.last_name(),
            username='user2',
            password='hola1234',
            email=fake.email(), 
            telephone=fake.phone_number(),
            photo=None
        
        )

        self.user_3 = User.objects.create_user(
            dni='12343399P',
            name=fake.name(),
            surname=fake.last_name(),
            username='user3',
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


        self.valoration_student = UserValoration.objects.create(
            value = 4,
            title = 'Title',
            review = 'Review del usuario 2',
            valuer = self.user,
            valued = self.user_2

        )

        self.valoration_student_2 = UserValoration.objects.create(
            value = 5,
            title = 'Titulo de ejemplo',
            review = 'Review del usuario 3',
            valuer = self.user,
            valued = self.user_3

        )

        self.valoration_student_3 = UserValoration.objects.create(
            value = 2,
            title = 'Titulo de ejemplo 2',
            review = 'Review del usuario 3',
            valuer = self.user_2,
            valued = self.user_3

        )


        login_user = {
            'username': self.user.username,
            'password': 'hola1234'
        }
        response_user = self.client.post('/login/',login_user, format='json')
        self.assertEqual(response_user.status_code, status.HTTP_200_OK)


        login_admin = {
            'username': self.admin.username,
            'password': 'developer'
        }
        response_admin = self.client.post('/login/', login_admin, format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_200_OK)
        
        self.token_user = response_user.data['access']
        self.token_admin = response_admin.data['access']



    def test_negative(self):
        response = self.client.get(f'/users/{self.user.id}/valorations/done/users')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.get(f'/users/{self.admin.id}/valorations/done/users')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.get(f'/users/{self.user_2.id}/valorations/done/users')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.get(f'/users/{self.user_2.id+10}/valorations/done/users')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_positive(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.get(f'/users/{self.user.id}/valorations/done/users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.valoration_student.id)
        self.assertEqual(response.data[1]['id'], self.valoration_student_2.id)
        self.assertEqual(len(response.data), 2)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.get(f'/users/{self.user_2.id}/valorations/done/users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.valoration_student_3.id)
        self.assertEqual(len(response.data), 1)

        