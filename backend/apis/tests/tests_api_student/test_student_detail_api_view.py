from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import Owner, User, Student

class TestStudentDetailApiView(APITestCase):

    
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
            dni='22337788L',
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
        self.token_admin = response_admin.data['access']
        self.token_student = response_student.data['access']




    ### GET BY ID

    def test_negative_get_one_student(self):
        response = self.client.get(f'/students/{self.owner.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.get(f'/students/{self.student_2.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.get(f'/students/{self.student.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.get(f'/students/{self.student_2.id+10}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  


    def test_positive_get_one_student(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.get(f'/students/{self.student.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.get(f'/students/{self.student.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)






    ### UPDATE

    def test_negative_update(self):
        response = self.client.put(f'/students/{self.student.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student_2.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/students/{self.student.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student_2.id+10}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        student_dni = {
            'dni': '223344551L',
            'name': self.student.name,
            'surname': self.student.surname,
            'username': self.student.username,
            'password': self.student.password,
            'email': self.student.email, 
            'telephone': self.student.telephone
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_dni)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)



        student_dni_2 = {
            'dni': 'ajklb123P',
            'name': self.student.name,
            'surname': self.student.surname,
            'username': self.student.username,
            'password': self.student.password,
            'email': self.student.email, 
            'telephone': self.student.telephone
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_dni_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)


        student_dni_exist = {
            'dni': '11223399P',
            'name': self.student.name,
            'surname': self.student.surname,
            'username': self.student.username,
            'password': self.student.password,
            'email': self.student.email, 
            'telephone': self.student.telephone
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_dni_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)



        student_dni_empty = {
            'dni': '',
            'name': self.student.name,
            'surname': self.student.surname,
            'username': self.student.username,
            'password': self.student.password,
            'email': self.student.email, 
            'telephone': self.student.telephone
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_dni_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)



        student_name = {
            'dni': self.student.dni,
            'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'surname': self.student.surname,
            'username': self.student.username,
            'password': self.student.password,
            'email': self.student.email, 
            'telephone': self.student.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(len(response.data), 1)



        student_name_empty = {
            'dni': self.student.dni,
            'name': '',
            'surname': self.student.surname,
            'username': self.student.username,
            'password': self.student.password,
            'email': self.student.email, 
            'telephone': self.student.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_name_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(len(response.data), 1)



        student_surname = {
            'dni': self.student.dni,
            'name': self.student.name,
            'surname': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'username': self.student.username,
            'password': self.student.password,
            'email': self.student.email, 
            'telephone': self.student.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_surname)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('surname', response.data)
        self.assertEqual(len(response.data), 1)



        student_surname_empty = {
            'dni': self.student.dni,
            'name': self.student.name,
            'surname': '',
            'username': self.student.username,
            'password': self.student.password,
            'email': self.student.email, 
            'telephone': self.student.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_surname_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('surname', response.data)
        self.assertEqual(len(response.data), 1)



        student_username = {
            'dni': self.student.dni,
            'name': self.student.name,
            'surname': self.student.surname,
            'username': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'password': self.student.password,
            'email': self.student.email, 
            'telephone': self.student.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_username)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)



        student_username_exist = {
            'dni': self.student.dni,
            'name': self.student.name,
            'surname': self.student.surname,
            'username': 'user2',
            'password': self.student.password,
            'email': self.student.email, 
            'telephone': self.student.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_username_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)



        student_username_empty = {
            'dni': self.student.dni,
            'name': self.student.name,
            'surname': self.student.surname,
            'username': '',
            'password': self.student.password,
            'email': self.student.email, 
            'telephone': self.student.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_username_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)


        student_email = {
            'dni': self.student.dni,
            'name': self.student.name,
            'surname': self.student.surname,
            'username': self.student.username,
            'password': self.student.password,
            'email': 'aaaaa.gmail.com',
            'telephone': self.student.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)



        student_email_exist = {
            'dni': self.student.dni,
            'name': self.student.name,
            'surname': self.student.surname,
            'username': self.student.username,
            'password': self.owner.password,
            'email': self.student_2.email,
            'telephone': self.student.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_email_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)



        student_email_empty = {
            'dni': self.student.dni,
            'name': self.student.name,
            'surname': self.student.surname,
            'username': self.student.username,
            'password': self.student.password,
            'email': '',
            'telephone': self.student.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_email_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)



        student_telephone = {
            'dni': self.student.dni,
            'name': self.student.name,
            'surname': self.student.surname,
            'username': self.student.username,
            'password': self.student.password,
            'email': self.student.email,
            'telephone': '666666666'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_telephone)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)



        student_telephone_2 = {
            'dni': self.student.dni,
            'name': self.student.name,
            'surname': self.student.surname,
            'username': self.student.username,
            'password': self.student.password,
            'email': self.student.email,
            'telephone': '+34666666a'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_telephone_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)



        student_telephone_empty = {
            'dni': self.student.dni,
            'name': self.student.name,
            'surname': self.student.surname,
            'username': self.student.username,
            'password': self.student.password,
            'email': self.student.email,
            'telephone': ''
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student_telephone_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)



        student_active = {
            'dni': self.student.dni,
            'name': self.student.name,
            'surname': self.student.surname,
            'username': self.student.username,
            'password': self.student.password,
            'email': self.student.email,
            'telephone': self.student.telephone,
            'isActive': False
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student_2.id}', student_active)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('No puede actualizar los datos de otro estudiante!', response.data['message'])
        self.assertEqual(len(response.data), 1)




    
    def test_positive_update(self):
        fake = Faker('es_ES')

        student = {
            'dni': '29874526P',
            'name': 'Nombre actualizado',
            'surname': 'Apellido nuevo',
            'username': 'usuarioPUT',
            'password': 'contraseña.put',
            'email': 'nuevoemail@hotmail.com',
            'telephone': '+34678091235',
            
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/students/{self.student.id}', student)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



        student_admin = {
            'dni': self.student.dni,
            'name': self.student.name,
            'surname': self.student.surname,
            'username': self.student.username,
            'password': self.student.password,
            'email': self.student.email,
            'telephone': self.student.telephone,
            'isAdministrator': True

        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.put(f'/students/{self.student_2.id}', student_admin)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



        student_admin_2 = {
            'dni': self.student.dni,
            'name': self.student.name,
            'surname': 'Surname Updated',
            'username': self.student.username,
            'password': self.student.password,
            'email': self.student.email,
            'telephone': self.student.telephone,

        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.put(f'/students/{self.student_2.id}', student_admin_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    ### DELETE

    def test_negative_delete(self):
        response = self.client.delete(f'/students/{self.student.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.delete(f'/students/{self.student_2.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.delete(f'/students/{self.student.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.delete(f'/students/{self.student_2.id+10}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_positive_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.delete(f'/students/{self.student.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.delete(f'/students/{self.student_2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
