from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import Owner, User, Student, Property, Photo, Rule, Service
from django.core.files.uploadedfile import SimpleUploadedFile

from tempfile import TemporaryDirectory
from django.conf import settings



class TestPropertyApiView(APITestCase):

    
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

        self.rule = Rule.objects.create(
            name = 'Regla 1',
        )

        self.service = Service.objects.create(
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

        self.property_owner_2 = Property.objects.create(
            title = 'Titulo',
            localization = 'Dirección Y',
            price = 200,
            type = 'Inmueble completo',
            dormitories = 4,
            size = 100,
            baths = 3,
            owner = self.owner,
        )

        self.property_owner.rules.set([self.rule])
        self.property_owner.photos.set([self.photo])
        self.property_owner.services.set([self.service])

        self.property_owner_2.photos.set([self.photo_2])

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
        response = self.client.get('/properties/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.property_owner.id)
        self.assertEqual(response.data[1]['id'], self.property_owner_2.id)
        self.assertEqual(len(response.data), 2)



    ### POST

    def test_negative_create(self):
        

        property = {
            'title':'Title',
            'localization': 'Dirección XYZ',
            'price': 177,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photo': self.photo.id,
        }
        response = self.client.post('/properties/', property)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post('/properties/', )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.post('/properties/', )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        property_title = {
            'title':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'localization': 'Dirección X',
            'price': 170,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_title)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertEqual(len(response.data), 1)


        property_title_empty = {
            'title':'',
            'localization': 'Dirección X',
            'price': 170,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_title_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertEqual(len(response.data), 1)


        property_localization = {
            'title':'Title',
            'localization': 'Dirección XDirección XDirección XDirección XDirección XDirección XDirección XDirección XDirección XXX',
            'price': 170,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_localization)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('localization', response.data)
        self.assertEqual(len(response.data), 1)


        property_localization_empty = {
            'title':'Title',
            'localization': '',
            'price': 170,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_localization_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('localization', response.data)
        self.assertEqual(len(response.data), 1)


        property_price = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 0,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_price)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)
        self.assertEqual(len(response.data), 1)

        property_price_2 = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': -2,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_price_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)
        self.assertEqual(len(response.data), 1)



        property_price_empty = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': '',
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_price_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)
        self.assertEqual(len(response.data), 1)


        property_type = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'Inmueble completoos',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('type', response.data)
        self.assertEqual(len(response.data), 1)


        property_type_2 = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'ICHC',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_type_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('type', response.data)
        self.assertEqual(len(response.data), 1)


        property_dormitories_empty = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'Habitacion',
            'dormitories': '',
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_dormitories_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dormitories', response.data)
        self.assertEqual(len(response.data), 1)


        property_dormitories_negative = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'Inmueble completo',
            'dormitories': -1,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_dormitories_negative)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dormitories', response.data)
        self.assertEqual(len(response.data), 1)



        property_size_empty = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'Habitacion',
            'dormitories': 3,
            'size': '', 
            'baths': 2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_size_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('size', response.data)
        self.assertEqual(len(response.data), 1)


        property_size_negative = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': -100, 
            'baths': 2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_size_negative)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('size', response.data)
        self.assertEqual(len(response.data), 1)



        property_baths_empty = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'Habitacion',
            'dormitories': 3,
            'size': 100, 
            'baths': '',
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_baths_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('baths', response.data)
        self.assertEqual(len(response.data), 1)


        property_baths_negative = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': -2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_baths_negative)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('baths', response.data)
        self.assertEqual(len(response.data), 1)


        property_student = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.post('/properties/', property_student)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(response.data), 1)


        property_photos = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_photos)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('photos', response.data)
        self.assertEqual(len(response.data), 1)


        property_photos_2 = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': ['aa'],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_photos_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('photos', response.data)
        self.assertEqual(len(response.data), 1)


        property_photos_3 = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': 'aaa',
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_photos_3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('photos', response.data)
        self.assertEqual(len(response.data), 1)


        property_services = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
            'services': 'cadena de texto'
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_services)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('services', response.data)
        self.assertEqual(len(response.data), 1)


        property_rules = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
            'rules': 'cadena de texto'
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_rules)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('rules', response.data)
        self.assertEqual(len(response.data), 1)


        property_unique = {
            'title': 'Titulo numero 2',
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': 2,
            'size': self.property_owner.size, 
            'baths': 1,
            'photos': [self.photo.id],
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_unique)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(len(response.data), 1)





    def test_positive_create(self):

        property = {
            'title':'Title',
            'localization': 'Dirección X',
            'price': 100,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id],
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        property_2 = {
            'title':'Title 3',
            'localization': 'Dirección X',
            'price': 210,
            'type': 'Inmueble completo',
            'dormitories': 3,
            'size': 200, 
            'baths': 2,
            'photos': [self.photo.id],
            'rules': [self.rule.id],
            'services': [self.service.id]

        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        property_max = {
            'title':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'localization': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'price': 100,
            'type': 'Habitacion',
            'dormitories': 3,
            'size': 100, 
            'baths': 2,
            'photos': [self.photo.id, self.photo.id],
            'rules': [self.rule.id],
            'services': [self.service.id]

        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_max)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        property_min = {
            'title':'a',
            'localization': 'a',
            'price': 1,
            'type': 'Cama',
            'dormitories': 0,
            'size': 0, 
            'baths': 0,
            'photos': [self.photo.id],
            'rules': [self.rule.id],
            'services': [self.service.id]

        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/properties/', property_min)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
  



    def tearDown(self):
        self.temp_dir.cleanup()

  



