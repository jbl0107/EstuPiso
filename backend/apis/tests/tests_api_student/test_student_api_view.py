from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import Owner, User, Student


class TestStudentApiView(APITestCase):

    
    def setUp(self):

        fake = Faker()
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



    def test_get_students(self):
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_positive_get_students(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    def test_negative_create_student(self):
        fake = Faker('es_ES')
        response = self.client.post('/students/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        student_admin = {
            'dni':'22334455C',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': 'developer12',
            'password': 'admin1234',
            'email': fake.email(), 
            'telephone': fake.phone_number(),
            'isAdministrator': 'true'
        }
        
        response = self.client.post('/students/', student_admin)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        self.assertEqual(len(response.data), 1)


        student_dni = {
            'dni':'223344551L',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_dni)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)


        student_dni_2 = {
            'dni': 'aa33LLaaQ',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_dni_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)


        student_dni_exist = {
            'dni':'22334455E',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password':'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_dni_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)


        student_dni_empty = {
            'dni': '',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_dni_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)


        student_name = {
            'dni': '22334445L',
            'name':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(len(response.data), 1)


        student_name_empty = {
            'dni': '22139445L',
            'name': '',
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_name_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(len(response.data), 1)



        student_surname = {
            'dni':'21334455L',
            'name': fake.name(),
            'surname': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'username': fake.user_name(),
            'password':'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_surname)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('surname', response.data)
        self.assertEqual(len(response.data), 1)


        student_surname_empty = {
            'dni': '22334405L',
            'name': fake.name(),
            'surname': '',
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_surname_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('surname', response.data)
        self.assertEqual(len(response.data), 1)



        student_username = {
            'dni': '12334455L',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone':fake.phone_number()
            
        }
        response = self.client.post('/students/', student_username)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)


        student_username_exist = {
            'dni': '12334455L',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': 'user1', 
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone':fake.phone_number()
            
        }
        response = self.client.post('/students/', student_username_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)


        student_username_empty = {
            'dni': '12345678A',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username':'',
            'password':'ejemplo112',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_username_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)



        student_password = {
            'dni': '11333355L',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(len(response.data), 1)


        student_password_2 = {
            'dni': '11333353L',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'aaaaaaa',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_password_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(len(response.data), 1)



        student_password_empty = {
            'dni': '12345678G',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': '',
            'email': fake.email(), 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_password_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(len(response.data), 1)


        student_email = {
            'dni': '10101010P',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': 'aaaaa.gmail.com', 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)



        student_email_exist = {
            'dni': '10101010P',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': self.owner.email, 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_email_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)



        student_email_empty = {
            'dni':'12345678P',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password':'ejemplo112',
            'email': '', 
            'telephone': fake.phone_number()
            
        }
        response = self.client.post('/students/', student_email_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)


        student_telephone = {
            'dni':'11009944S',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone':'666666666'
            
        }
        response = self.client.post('/students/', student_telephone)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)


        student_telephone_2 = {
            'dni':'11009744S',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password': 'ejemplo112',
            'email': fake.email(), 
            'telephone': '+34666666'
            
        }
        response = self.client.post('/students/', student_telephone_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)


        student_telephone_empty = {
            'dni':'12345678J',
            'name': fake.name(),
            'surname': fake.last_name(),
            'username': fake.user_name(),
            'password':'ejemplo112',
            'email': fake.email(), 
            'telephone': ''
            
        }
        response = self.client.post('/students/', student_telephone_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)



        



    def test_positive_create_student(self):
        fake = Faker('es_ES')
        
        student = {
            'dni':'22334455L',
            'name':fake.name(),
            'surname':fake.last_name(),
            'username':'usuario',
            'password':'user1234',
            'email': fake.email(), 
            'telephone':fake.phone_number()
            
        }
        response = self.client.post('/students/', student)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        student_max = {
            'dni':'22930415L',
            'name':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'surname':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'username':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'password':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'email': fake.email(), 
            'telephone':fake.phone_number()
            
        }
        response = self.client.post('/students/', student_max)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        student_min = {
            'dni':'01133447L',
            'name':'a',
            'surname':'a',
            'username':'a',
            'password':'aaaaaaaa',
            'email': fake.email(), 
            'telephone':fake.phone_number()
            
        }
        response = self.client.post('/students/', student_min)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



