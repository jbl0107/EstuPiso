from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import Owner, User, Student, Property, Photo, Service
from django.core.files.uploadedfile import SimpleUploadedFile

from tempfile import TemporaryDirectory
from django.conf import settings



class TestPropertyServicesApiView(APITestCase):

    
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

        self.image = SimpleUploadedFile(name='test_image.jpg', content=open('backend/tests/tests_api_owner/test_image.jpg', 'rb').read(), 
                                   content_type='image/jpeg')
        
        self.image_2 = SimpleUploadedFile(name='test_image_2.jpg', content=open(
            'backend/tests/tests_api_owner/test_image_2.jpg', 'rb').read(), content_type='image/jpeg')


        self.photo = Photo.objects.create(
            photo = self.image,
            owner = self.owner
        )

        self.photo_2 = Photo.objects.create(
            photo = self.image_2,
            owner = self.owner
        )

        self.service = Service.objects.create(
            name = 'Servicio 1',
        )

        self.service_2 = Service.objects.create(
            name = 'Servicio 2',
        )

        self.service_3 = Service.objects.create(
            name = 'Servicio 3',
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

        self.property_owner_2 = Property.objects.create(
            title = 'Titulo',
            localization = 'Dirección Y',
            price = 200,
            type = 'Inmueble completo',
            dormitories = 4,
            size = 100,
            baths = 3,
            owner = self.owner_2,
        )

        self.property_owner.services.set([self.service, self.service_2, self.service_3])
        self.property_owner.photos.set([self.photo])

        self.property_owner_2.photos.set([self.photo_2])
        self.property_owner_2.services.set([self.service_2])



    def test_negative(self):
        response = self.client.get(f'/properties/{self.property_owner_2.id+10}/services')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_positive(self):
        expected_service_ids = [self.service.id, self.service_2.id, self.service_3.id]
        response = self.client.get(f'/properties/{self.property_owner.id}/services')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_service_ids = [service['id'] for service in response.data]
        self.assertCountEqual(returned_service_ids, expected_service_ids)

        response = self.client.get(f'/properties/{self.property_owner_2.id}/services')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.service_2.id)




    def tearDown(self):
        self.temp_dir.cleanup()