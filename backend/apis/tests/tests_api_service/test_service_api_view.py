from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import Owner, User, Student, Service





class TestServiceApiView(APITestCase):

    
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
        

        self.service = Service.objects.create(
            name = 'Regla 1',
        )

        self.service_2 = Service.objects.create(
            name = 'Regla 2',
        )

        self.service_3 = Service.objects.create(
            name = 'Regla 3',
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
        expected_service_ids = [self.service.id, self.service_2.id, self.service_3.id]

        response = self.client.get('/services/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_service_ids = [service['id'] for service in response.data]
        self.assertCountEqual(returned_service_ids, expected_service_ids)

       



    ### POST

    def test_negative_create(self):
        response = self.client.post('/services/', )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        service_max = {
            'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post('/services/', service_max)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        service_min = {
            'name': ''
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post('/services/', service_min)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post('/services/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.post('/services/', )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/services/', {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




    def test_positive_create(self):

        service_max = {
            'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post('/services/', service_max)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        service_min = {
            'name': 'r'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post('/services/', service_min)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        service_4 = {
            'name': 'regla 4'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post('/services/', service_4)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



