from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import User

class TestUserApiView(APITestCase):

    
    def setUp(self):

        fake = Faker()
        self.user = User.objects.create_user(
            dni='22334455E',
            name=fake.name(),
            surname=fake.last_name(),
            username='user1',
            password='hola1234',
            email=fake.email(), 
            telephone=fake.phone_number(),
            photo=None
        
        )
        self.admin = User.objects.create_superuser(
            dni='22334455A',
            name='Developer',
            surname='Developer',
            username='developer',
            password='developer',
            email=fake.email(), 
            telephone=fake.phone_number(),
            photo=None
        )

        login_user = {
            'username': self.user.username,
            'password': 'hola1234'
        }
        response_user = self.client.post('/login/',login_user, format='json')
        self.assertEqual(response_user.status_code, status.HTTP_200_OK)


        login_admin = {
            'username': self.admin.username,
            'password': 'developer'
        }
        response_admin = self.client.post('/login/', login_admin, format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_200_OK)
        
        self.token_user = response_user.data['access']
        self.token_admin = response_admin.data['access']



    def test_negative_get_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        
    def test_positive_get_users(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    def test_negative_create_user(self):
        fake = Faker('es_ES')
        response = self.client.post('/users/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        admin = {
            'dni':'22334455C',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': 'developer12',
            'password': 'admin1234',
            'email': fake.email(), 
            'telephone': fake.phone_number(),
            'isAdministrator': 'true'
        }
        
        response = self.client.post('/users/', admin)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('message', response.data)
        self.assertEqual(len(response.data), 1)


        user_dni = {
            'dni':'223344551L',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_dni)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)


        user_dni_2 = {
            'dni': 'aa33LLaaQ',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_dni_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)


        user_dni_exist = {
            'dni':'22334455E', #del user del setUp
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password':'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_dni_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)


        user_dni_empty = {
            'dni': '',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_dni_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)


        user_name = {
            'dni': '22334445L',
            'name':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(len(response.data), 1)


        user_name_empty = {
            'dni': '22139445L',
            'name': '',
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_name_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(len(response.data), 1)



        user_surname = {
            'dni':'21334455L',
            'name': fake.name(),
            'surname': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'username': fake.user_name(),
            'password':'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_surname)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('surname', response.data)
        self.assertEqual(len(response.data), 1)


        user_surname_empty = {
            'dni': '22334405L',
            'name': fake.name(),
            'surname': '',
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_surname_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('surname', response.data)
        self.assertEqual(len(response.data), 1)



        user_username = {
            'dni': '12334455L',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone':fake.phone_number()
            
        }
        response = self.client.post('/users/', user_username)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)


        user_username_exist = {
            'dni': '12334455L',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': 'user1', 
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone':fake.phone_number()
            
        }
        response = self.client.post('/users/', user_username_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)


        user_username_empty = {
            'dni': '12345678A',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username':'',
            'password':'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_username_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)



        user_password = {
            'dni': '11333355L',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(len(response.data), 1)


        user_password_2 = {
            'dni': '11333353L',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'aaaaaaa',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_password_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(len(response.data), 1)



        user_password_empty = {
            'dni': '12345678G',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': '',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_password_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(len(response.data), 1)


        user_email = {
            'dni': '10101010P',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': 'aaaaa.gmail.com', 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)



        user_email_exist = {
            'dni': '10101010P',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': self.user.email, 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_email_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)



        user_email_empty = {
            'dni':'12345678P',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password':'ejemplo112',
            'email': '', 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/users/', user_email_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)


        user_telephone = {
            'dni':'11009944S',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone':'666666666'
            
        }
        response = self.client.post('/users/', user_telephone)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)


        user_telephone_2 = {
            'dni':'11009744S',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone': '+34666666'
            
        }
        response = self.client.post('/users/', user_telephone_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)


        user_telephone_empty = {
            'dni':'12345678J',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password':'ejemplo112',
            'email': fake.email(), 
            'telephone': ''
            
        }
        response = self.client.post('/users/', user_telephone_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)


        user_admin = {
            'dni':'12345678J',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password':'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number(),
            'isAdministrator': True
            
        }
        response = self.client.post('/users/', user_admin)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('No puede crear un administrador. Contacte con alguno para que este le de permisos de administrador', 
                         response.data['message'])
        self.assertEqual(len(response.data), 1)

        



    def test_positive_create_user(self):
        fake = Faker('es_ES')
        
        user = {
            'dni':'22334455L',
            'name':fake.name(),
            'surname':fake.last_name(),
            'username':'usuario',
            'password':'user1234',
            'email': fake.email(), 
            'telephone':fake.phone_number()
            
        }
        response = self.client.post('/users/', user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        user_max = {
            'dni':'22930415L',
            'name':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'surname':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'username':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'password':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'email': fake.email(), 
            'telephone':fake.phone_number()
            
        }
        response = self.client.post('/users/', user_max)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        user_min = {
            'dni':'01133447L',
            'name':'a',
            'surname':'a',
            'username':'a',
            'password':'aaaaaaaa',
            'email': fake.email(), 
            'telephone':fake.phone_number()
            
        }
        response = self.client.post('/users/', user_min)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



