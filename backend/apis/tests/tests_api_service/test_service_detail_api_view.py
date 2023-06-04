from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import Owner, User, Student, Service





class TestRuleDetailApiView(APITestCase):

    
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


        
    ###GET BY ID

    def test_negative_get(self):
        response = self.client.get(f'/services/{self.service.id+10}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_positive_get(self):
        response = self.client.get(f'/services/{self.service.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


       

    ### PUT

    def test_negative_put(self):
        response = self.client.put(f'/services/{self.service.id}', )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        rule_max = {
            'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.put(f'/services/{self.service.id}', rule_max)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(len(response.data), 1)


        rule_min = {
            'name': ''
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.put(f'/services/{self.service.id}', rule_min)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(len(response.data), 1)


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.put(f'/services/{self.service.id}', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/services/{self.service.id}', )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/services/{self.service.id}', {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_positive_put(self):

        service_max = {
            'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.put(f'/services/{self.service.id}', service_max)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        service_min = {
            'name': 'r'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.put(f'/services/{self.service_2.id}', service_min)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        service_3_2 = {
            'name': 'regla 3 actualizada'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.put(f'/services/{self.service_3.id}', service_3_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    
    ###DELETE

    def test_negative_delete(self):
        response = self.client.delete(f'/services/{self.service.id}', )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.delete(f'/services/{self.service.id+10}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.delete(f'/services/{self.service.id}', )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.delete(f'/services/{self.service.id}', {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_positive_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.delete(f'/services/{self.service.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.delete(f'/services/{self.service_2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)




