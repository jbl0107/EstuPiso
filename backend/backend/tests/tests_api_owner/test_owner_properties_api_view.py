from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import Owner, User, Property, Photo, Rule, Service, Student
from django.core.files.uploadedfile import SimpleUploadedFile

from tempfile import TemporaryDirectory
from django.conf import settings


class TestOwnerPropertiesApiView(APITestCase):

    
    def setUp(self):

        self.temp_dir = TemporaryDirectory()
        settings.MEDIA_ROOT = self.temp_dir.name
        
        image = SimpleUploadedFile(name='test_image.jpg', content=open('backend/tests/tests_api_owner/test_image.jpg', 'rb').read(), 
                                   content_type='image/jpeg')
        
        image_2 = SimpleUploadedFile(name='test_image_2.jpg', content=open(
            'backend/tests/tests_api_owner/test_image_2.jpg', 'rb').read(), content_type='image/jpeg')


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

        photo = Photo.objects.create(
            photo = image,
            owner = self.owner
        )

        photo_2 = Photo.objects.create(
            photo = image_2,
            owner = self.owner_2
        )

        rule = Rule.objects.create(
            name = 'Regla 1',
        )

        service = Service.objects.create(
            name = 'Servicio 1',
        )


        self.property_owner = Property.objects.create(
            title = 'titulo de ejemplo',
            localization = 'Dirección X',
            price = 170,
            type = 'Inmueble completo',
            dormitories = 3,
            size = 100,
            baths = 2,
            owner = self.owner,
        )
        self.property_owner.rules.set([rule])
        self.property_owner.photos.set([photo])
        self.property_owner.services.set([service])



        self.property_owner_2 = Property.objects.create(
            title = 'titulo 1',
            localization = 'Dirección A',
            price = 140,
            type = 'Habitación',
            dormitories = 2,
            size = 60,
            baths = 1,
            owner = self.owner_2,
        )
        self.property_owner_2.photos.set([photo_2])
        

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
        self.token_admin = response_admin.data['access']
        self.token_student = response_student.data['access']



    def test_negative(self):
        response = self.client.get(f'/owners/{self.owner.id}/properties')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.get(f'/owners/{self.owner_2.id}/properties')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.get(f'/owners/{self.owner.id}/properties')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.get(f'/owners/{self.owner_2.id+10}/properties')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  

    def test_positive(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.get(f'/owners/{self.owner.id}/properties')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['id'], self.property_owner.id)


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.get(f'/owners/{self.owner_2.id}/properties')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['id'], self.property_owner_2.id)


    def tearDown(self):
        self.temp_dir.cleanup()