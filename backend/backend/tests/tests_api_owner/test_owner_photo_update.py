from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import Owner, User, Student
from django.core.files.uploadedfile import SimpleUploadedFile

from tempfile import TemporaryDirectory
from django.conf import settings



class TestOwnerPhotoUpdate(APITestCase):

    
    def setUp(self):

        self.temp_dir = TemporaryDirectory()
        settings.MEDIA_ROOT = self.temp_dir.name

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


        self.student = Student.objects.create_user(
            dni='22337788O',
            name=fake.name(),
            surname=fake.last_name(),
            username='student',
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


        login_owner = {
            'username': self.owner.username,
            'password': 'hola1234'
        }
        response_owner = self.client.post('/login/',login_owner, format='json')
        self.assertEqual(response_owner.status_code, status.HTTP_200_OK)


        login_student = {
            'username': self.student.username,
            'password': 'hola1234'
        }
        response_student = self.client.post('/login/',login_student, format='json')
        self.assertEqual(response_student.status_code, status.HTTP_200_OK)


        login_admin = {
            'username': self.admin.username,
            'password': 'developer'
        }
        response_admin = self.client.post('/login/', login_admin, format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_200_OK)
        
        self.token_owner = response_owner.data['access']
        self.token_student = response_student.data['access']
        self.token_admin = response_admin.data['access']




    def test_negative(self):
        response = self.client.put(f'/owners/photo-update/{self.owner.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/owners/photo-update/{self.owner.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/photo-update/{self.owner_2.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        photo = {
            'photo': 'image'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/photo-update/{self.owner.id}', photo)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/photo-update/{self.owner_2.id+10}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_positive(self):

        image = SimpleUploadedFile(name='test_image.jpg', content=open('backend/tests/tests_api_owner/test_image.jpg', 'rb').read(), 
                                   content_type='image/jpeg')
        
        

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        photo = {
            'photo': image
        }
        response = self.client.put(f'/owners/photo-update/{self.owner.id}', photo)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        photo = {
            'photo': ''
        }
        response = self.client.put(f'/owners/photo-update/{self.owner.id}', photo)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        photo = {
            'photo': image
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.put(f'/owners/photo-update/{self.owner_2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
  

    def tearDown(self):
        self.temp_dir.cleanup()

  



