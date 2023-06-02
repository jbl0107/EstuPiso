from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import Owner, User


class TestOwnerPublicDetailApiView(APITestCase):

    
    def setUp(self):


        fake = Faker('es_ES')
        self.owner = Owner.objects.create_user(
            dni='22334455E',
            name=fake.name(),
            surname=fake.last_name(),
            username='user1',
            password='hola1234',
            email=fake.email(), 
            telephone=fake.phone_number(),
            photo=None
        
        )

        self.owner_2 = Owner.objects.create_user(
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





    def test_negative(self):
        response = self.client.get(f'/owners/{self.owner_2.id+10}/public')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_positive(self):
        response = self.client.get(f'/owners/{self.owner.id}/public')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        response = self.client.get(f'/owners/{self.owner_2.id}/public')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
