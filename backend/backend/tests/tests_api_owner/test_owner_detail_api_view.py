from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import Owner, User, Student

class TestOwnerDetailApiView(APITestCase):

    
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

    def test_negative_get_one_owner(self):
        response = self.client.get(f'/owners/{self.owner.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.get(f'/owners/{self.owner_2.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.get(f'/owners/{self.owner.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.get(f'/owners/{self.owner_2.id+10}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  


    def test_positive_get_one_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.get(f'/owners/{self.owner.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.get(f'/owners/{self.owner.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)






    ### UPDATE

    def test_negative_update(self):
        response = self.client.put(f'/owners/{self.owner.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner_2.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.put(f'/owners/{self.owner.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner_2.id+10}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        owner_dni = {
            'dni': '223344551L',
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner.email, 
            'telephone': self.owner.telephone
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_dni)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)



        owner_dni_2 = {
            'dni': 'ajklb123P',
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner.email, 
            'telephone': self.owner.telephone
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_dni_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)


        owner_dni_exist = {
            'dni': '11223399P',
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner.email, 
            'telephone': self.owner.telephone
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_dni_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)



        owner_dni_empty = {
            'dni': '',
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner.email, 
            'telephone': self.owner.telephone
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_dni_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)



        owner_name = {
            'dni': self.owner.dni,
            'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'surname': self.owner.surname,
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner.email, 
            'telephone': self.owner.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(len(response.data), 1)



        owner_name_empty = {
            'dni': self.owner.dni,
            'name': '',
            'surname': self.owner.surname,
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner.email, 
            'telephone': self.owner.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_name_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(len(response.data), 1)



        owner_surname = {
            'dni': self.owner.dni,
            'name': self.owner.name,
            'surname': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner.email, 
            'telephone': self.owner.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_surname)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('surname', response.data)
        self.assertEqual(len(response.data), 1)



        owner_surname_empty = {
            'dni': self.owner.dni,
            'name': self.owner.name,
            'surname': '',
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner.email, 
            'telephone': self.owner.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_surname_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('surname', response.data)
        self.assertEqual(len(response.data), 1)



        owner_username = {
            'dni': self.owner.dni,
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'password': self.owner.password,
            'email': self.owner.email, 
            'telephone': self.owner.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_username)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)



        owner_username_exist = {
            'dni': self.owner.dni,
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': 'user2',
            'password': self.owner.password,
            'email': self.owner.email, 
            'telephone': self.owner.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_username_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)



        owner_username_empty = {
            'dni': self.owner.dni,
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': '',
            'password': self.owner.password,
            'email': self.owner.email, 
            'telephone': self.owner.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_username_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)


        owner_email = {
            'dni': self.owner.dni,
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': self.owner.username,
            'password': self.owner.password,
            'email': 'aaaaa.gmail.com',
            'telephone': self.owner.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)



        owner_email_exist = {
            'dni': self.owner.dni,
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner_2.email,
            'telephone': self.owner.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_email_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)



        owner_email_empty = {
            'dni': self.owner.dni,
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': self.owner.username,
            'password': self.owner.password,
            'email': '',
            'telephone': self.owner.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_email_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)



        owner_telephone = {
            'dni': self.owner.dni,
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner.email,
            'telephone': '666666666'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_telephone)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)



        owner_telephone_2 = {
            'dni': self.owner.dni,
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner.email,
            'telephone': '+34666666a'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_telephone_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)



        owner_telephone_empty = {
            'dni': self.owner.dni,
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner.email,
            'telephone': ''
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner_telephone_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)



        owner_active = {
            'dni': self.owner.dni,
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner.email,
            'telephone': self.owner.telephone,
            'isActive': False
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner_2.id}', owner_active)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('No puede cambiar los datos de otro propietario que no sea usted mismo', response.data['message'])
        self.assertEqual(len(response.data), 1)




    
    def test_positive_update(self):
        fake = Faker('es_ES')

        owner = {
            'dni': '29874526P',
            'name': 'Nombre actualizado',
            'surname': 'Apellido nuevo',
            'username': 'usuarioPUT',
            'password': 'contraseña.put',
            'email': 'nuevoemail@hotmail.com',
            'telephone': '+34678091235',
            
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.put(f'/owners/{self.owner.id}', owner)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



        owner_admin = {
            'dni': self.owner.dni,
            'name': self.owner.name,
            'surname': self.owner.surname,
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner.email,
            'telephone': self.owner.telephone,
            'isAdministrator': True

        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.put(f'/owners/{self.owner_2.id}', owner_admin)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



        owner_admin_2 = {
            'dni': self.owner.dni,
            'name': self.owner.name,
            'surname': 'Surname Updated',
            'username': self.owner.username,
            'password': self.owner.password,
            'email': self.owner.email,
            'telephone': self.owner.telephone,

        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.put(f'/owners/{self.owner_2.id}', owner_admin_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    ### DELETE

    def test_negative_delete(self):
        response = self.client.delete(f'/owners/{self.owner.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.delete(f'/owners/{self.owner_2.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_student)
        response = self.client.delete(f'/owners/{self.owner.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.delete(f'/owners/{self.owner_2.id+10}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_positive_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_owner)
        response = self.client.delete(f'/owners/{self.owner.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.delete(f'/owners/{self.owner_2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
