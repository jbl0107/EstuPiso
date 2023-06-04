from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import Owner, User, Student, Property, Photo, Rule, Service
from django.core.files.uploadedfile import SimpleUploadedFile

from tempfile import TemporaryDirectory
from django.conf import settings



class TestPropertyDetailApiView(APITestCase):

    
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
            owner = self.owner_2,
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


    ### GET BY ID

    def test_negative_get_by_id(self):
        response = self.client.get(f'/properties/{self.property_owner_2.id+10}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_positive_get_by_id(self):
        response = self.client.get(f'/properties/{self.property_owner.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f'/properties/{self.property_owner_2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    ### PUT

    def test_negative_update(self):
        

        property = {
            'title': 'Titulo numero 222',
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }
        response = self.client.put(f'/properties/{self.property_owner.id}', property)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner_2.id}', property)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.put(f'/properties/{self.property_owner.id}', )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/properties/{self.property_owner.id}', )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        property_title = {
            'title': 'Update tituloUpdate tituloUpdate tituloUpdate titul',
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_title)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertEqual(len(response.data), 1)


        property_title_empty = {
            'title': '',
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_title_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertEqual(len(response.data), 1)


        property_localization = {
            'title': self.property_owner.title,
            'localization': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_localization)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('localization', response.data)
        self.assertEqual(len(response.data), 1)


        property_localization_empty = {
            'title': self.property_owner.title,
            'localization': '',
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_localization_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('localization', response.data)
        self.assertEqual(len(response.data), 1)


        property_price = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': 0,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_price)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)
        self.assertEqual(len(response.data), 1)

        property_price_2 = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': -2,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_price_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)
        self.assertEqual(len(response.data), 1)



        property_price_empty = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': '',
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_price_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)
        self.assertEqual(len(response.data), 1)


        property_type = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': 'Inmueble completoosss',
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('type', response.data)
        self.assertEqual(len(response.data), 1)


        property_type_2 = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': 'ICHC',
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_type_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('type', response.data)
        self.assertEqual(len(response.data), 1)


        property_dormitories_empty = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': '',
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_dormitories_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dormitories', response.data)
        self.assertEqual(len(response.data), 1)


        property_dormitories_negative = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': -1,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_dormitories_negative)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dormitories', response.data)
        self.assertEqual(len(response.data), 1)



        property_size_empty = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': '', 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_size_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('size', response.data)
        self.assertEqual(len(response.data), 1)


        property_size_negative = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': -1, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_size_negative)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('size', response.data)
        self.assertEqual(len(response.data), 1)



        property_baths_empty = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': '',
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_baths_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('baths', response.data)
        self.assertEqual(len(response.data), 1)


        property_baths_negative = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': -1,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_baths_negative)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('baths', response.data)
        self.assertEqual(len(response.data), 1)


        property_student = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_student)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(response.data), 1)


        property_photos = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_photos)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('photos', response.data)
        self.assertEqual(len(response.data), 1)


        property_photos_2 = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': ['abcd'],
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_photos_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('photos', response.data)
        self.assertEqual(len(response.data), 1)


        property_photos_3 = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': 'aaa',
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_photos_3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('photos', response.data)
        self.assertEqual(len(response.data), 1)


        property_services = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
            'services': 'cadena de texto'
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_services)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('services', response.data)
        self.assertEqual(len(response.data), 1)


        property_rules = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
            'rules': 'cadena de texto'
        }


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_rules)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('rules', response.data)
        self.assertEqual(len(response.data), 1)


        property_unique = {
            'title': self.property_owner.title,
            'localization': self.property_owner_2.localization,
            'price': self.property_owner_2.price,
            'type': self.property_owner_2.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner_2.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_unique)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(len(response.data), 1)





    def test_positive_update(self):

        property = {
            'title': 'Title update',
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': 100, 
            'baths': 5,
            'photos': [self.photo.id],
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        property_2 = {
            'title': self.property_owner.title,
            'localization': self.property_owner.localization,
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],

            'rules': [self.rule.id],
            'services': [self.service.id]

        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        property_max = {
            'title': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'localization': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'price': self.property_owner.price,
            'type': self.property_owner.type,
            'dormitories': self.property_owner.dormitories,
            'size': self.property_owner.size, 
            'baths': self.property_owner.baths,
            'photos': [self.photo.id],
            'rules': [self.rule.id],
            'services': [self.service.id]

        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_max)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        property_min = {
            'title': 'a',
            'localization': 'a',
            'price': 1,
            'type': self.property_owner.type,
            'dormitories': 0,
            'size': 0, 
            'baths': 0,
            'photos': [self.photo.id],
            'rules': [self.rule.id],
            'services': [self.service.id]

        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/properties/{self.property_owner.id}', property_min)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
  



    ### DELETE

    def test_negative_delete(self):
        response = self.client.delete(f'/properties/{self.property_owner.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.delete(f'/properties/{self.property_owner_2.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.delete(f'/properties/{self.property_owner.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.delete(f'/properties/{self.property_owner_2.id+10}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_positive_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.delete(f'/properties/{self.property_owner.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.delete(f'/properties/{self.property_owner_2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.temp_dir.cleanup()

  



