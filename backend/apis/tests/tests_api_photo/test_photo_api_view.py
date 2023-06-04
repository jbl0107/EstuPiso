from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import Owner, User, Student, Photo
from django.core.files.uploadedfile import SimpleUploadedFile

from tempfile import TemporaryDirectory
from django.conf import settings




class TestPhotoApiView(APITestCase):

    
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

        self.image = SimpleUploadedFile(name='test_image.jpg', content=open('apis/tests/tests_api_owner/test_image.jpg', 'rb').read(), 
                                   content_type='image/jpeg')
        
        self.image_2 = SimpleUploadedFile(name='test_image_2.jpg', content=open(
            'apis/tests/tests_api_owner/test_image_2.jpg', 'rb').read(), content_type='image/jpeg')
        

        self.photo = Photo.objects.create(
            photo = self.image,
            owner = self.owner
        )

        self.photo_2 = Photo.objects.create(
            photo = self.image_2,
            owner = self.owner
        )

        self.photo_3 = Photo.objects.create(
            photo = self.image_2,
            owner = self.owner
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


    ### GET ALL


        
    def test_positive_get_all(self):
        expected_photo_ids = [self.photo.id, self.photo_2.id, self.photo_3.id]

        response = self.client.get('/photos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_photo_ids = [photo['id'] for photo in response.data]
        self.assertCountEqual(returned_photo_ids, expected_photo_ids)

       



    ### POST

    def test_negative_create(self):
        
         #para que el archivo en sí no este "vacío" y de error, hay que crear la imagen aquí
        image_negative = SimpleUploadedFile(name='test_image.jpg', content=open('apis/tests/tests_api_owner/test_image.jpg', 'rb').read(), 
                                   content_type='image/jpeg')


        photo = {
            'photo': image_negative
            
        }
        response = self.client.post('/photos/', photo)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/photos/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post('/photos/', )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.post('/photos/', )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        photo_empty = {
            'photo':'',
            
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/photos/', photo_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_positive_create(self):
        
        #para que el archivo en sí no este "vacío" y de error, hay que crear la imagen aquí
        image_positive = SimpleUploadedFile(name='test_image.jpg', content=open('apis/tests/tests_api_owner/test_image.jpg', 'rb').read(), 
                                   content_type='image/jpeg')

        photo = {
            'photo':image_positive
            
        }



        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/photos/', photo)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    def tearDown(self):
        self.temp_dir.cleanup()