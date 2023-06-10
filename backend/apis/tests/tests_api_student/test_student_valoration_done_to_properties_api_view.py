from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import Owner, User, Student, PropertyValoration, Property, Photo, Rule, Service

from django.core.files.uploadedfile import SimpleUploadedFile

from tempfile import TemporaryDirectory
from django.conf import settings


class TestStudentVerifyPassword(APITestCase):

    
    def setUp(self):

        self.temp_dir = TemporaryDirectory()
        settings.MEDIA_ROOT = self.temp_dir.name
        
        image = SimpleUploadedFile(name='test_image.jpg', content=open('apis/tests/tests_api_owner/test_image.jpg', 'rb').read(), 
                                   content_type='image/jpeg')
        
        

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

        self.student_2 = Student.objects.create_user(
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

        photo = Photo.objects.create(
            photo = image,
            owner = self.owner
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

        self.valoration_student = PropertyValoration.objects.create(
            value = 4,
            title = 'Title',
            review = 'Esto es una opinion de ejemplo',
            valuer = self.student,
            property = self.property_owner

        )

        self.valoration_student_2 = PropertyValoration.objects.create(
            value = 5,
            title = 'Titulo de ejemplo',
            review = 'Review de la property',
            valuer = self.student_2,
            property = self.property_owner

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
        response = self.client.get(f'/students/{self.student.id}/valorations/done/properties/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.get(f'/students/{self.student.id}/valorations/done/properties/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.get(f'/students/{self.student_2.id}/valorations/done/properties/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_positive(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
       
        response = self.client.get(f'/students/{self.student.id}/valorations/done/properties/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.valoration_student.id)
        self.assertEqual(len(response.data), 1)


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.get(f'/students/{self.student_2.id}/valorations/done/properties/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.valoration_student_2.id)
        self.assertEqual(len(response.data), 1)
  

  
    def tearDown(self):
            self.temp_dir.cleanup()


