from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import Owner, User, Student, Rule





class TestRuleApiView(APITestCase):

    
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
        

        self.rule = Rule.objects.create(
            name = 'Regla 1',
        )

        self.rule_2 = Rule.objects.create(
            name = 'Regla 2',
        )

        self.rule_3 = Rule.objects.create(
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
        expected_rule_ids = [self.rule.id, self.rule_2.id, self.rule_3.id]

        response = self.client.get('/rules/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_rule_ids = [rule['id'] for rule in response.data]
        self.assertCountEqual(returned_rule_ids, expected_rule_ids)

       



    ### POST

    def test_negative_create(self):
        response = self.client.post('/rules/', )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        rule_max = {
            'name': 'regla con el maximo de caracteresregla con el maximo de caracteresregla con el maximo de caracteresss'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post('/rules/', rule_max)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        rule_min = {
            'name': ''
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post('/rules/', rule_min)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post('/rules/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.post('/rules/', )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.post('/rules/', {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




    def test_positive_create(self):

        rule_max = {
            'name': 'regla con el maximo de caracteresregla con el maximo de caracteresregla con el maximo de caracteress'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post('/rules/', rule_max)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        rule_min = {
            'name': 'r'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post('/rules/', rule_min)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        rule_4 = {
            'name': 'regla 4'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.post('/rules/', rule_4)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



