from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apis.models import User

class TestUserDetailApiView(APITestCase):

    
    def setUp(self):

        fake = Faker('es_ES')
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

        self.user_2 = User.objects.create_user(
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




    ### GET BY ID

    def test_negative_get_one_user(self):
        response = self.client.get(f'/users/{self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.get(f'/users/{self.admin.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.get(f'/users/{self.user_2.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.get(f'/users/{self.user_2.id+10}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

  


    def test_positive_get_one_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.get(f'/users/{self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.get(f'/users/{self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.get(f'/users/{self.admin.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)






    ### UPDATE

    def test_negative_update(self):
        response = self.client.put(f'/users/{self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.admin.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user_2.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user_2.id+10}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        user_dni = {
            'dni': '223344551L',
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email, 
            'telephone': self.user.telephone
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_dni)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)



        user_dni_2 = {
            'dni': 'ajklb123P',
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email, 
            'telephone': self.user.telephone
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_dni_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)


        user_dni_exist = {
            'dni': '11223399P',
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email, 
            'telephone': self.user.telephone
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_dni_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)



        user_dni_empty = {
            'dni': '',
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email, 
            'telephone': self.user.telephone
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_dni_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('dni', response.data)
        self.assertEqual(len(response.data), 1)



        user_name = {
            'dni': self.user.dni,
            'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email, 
            'telephone': self.user.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(len(response.data), 1)



        user_name_empty = {
            'dni': self.user.dni,
            'name': '',
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email, 
            'telephone': self.user.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_name_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(len(response.data), 1)



        user_surname = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email, 
            'telephone': self.user.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_surname)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('surname', response.data)
        self.assertEqual(len(response.data), 1)



        user_surname_empty = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': '',
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email, 
            'telephone': self.user.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_surname_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('surname', response.data)
        self.assertEqual(len(response.data), 1)



        user_username = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'password': self.user.password,
            'email': self.user.email, 
            'telephone': self.user.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_username)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)



        user_username_exist = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': 'user2',
            'password': self.user.password,
            'email': self.user.email, 
            'telephone': self.user.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_username_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)



        user_username_empty = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': '',
            'password': self.user.password,
            'email': self.user.email, 
            'telephone': self.user.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_username_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertEqual(len(response.data), 1)



        user_password = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'email': self.user.email, 
            'telephone': self.user.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(len(response.data), 1)



        user_password_2 = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': 'aaaaaaa',
            'email': self.user.email, 
            'telephone': self.user.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_password_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(len(response.data), 1)



        user_password_empty = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': '',
            'email': self.user.email, 
            'telephone': self.user.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_password_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(len(response.data), 1)



        user_email = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': 'aaaaa.gmail.com',
            'telephone': self.user.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)



        user_email_exist = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user_2.email,
            'telephone': self.user.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_email_exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)



        user_email_empty = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': '',
            'telephone': self.user.telephone

        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_email_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(len(response.data), 1)



        user_telephone = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email,
            'telephone': '666666666'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_telephone)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)



        user_telephone_2 = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email,
            'telephone': '+34666666a'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_telephone_2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)



        user_telephone_empty = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email,
            'telephone': ''
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_telephone_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('telephone', response.data)
        self.assertEqual(len(response.data), 1)


        user_admin = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email,
            'telephone': self.user.telephone,
            'isAdministrator': True
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user_admin)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('No puede hacerse administrador a si mismo', response.data['message'])
        self.assertEqual(len(response.data), 1)


        user_admin_2 = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email,
            'telephone': self.user.telephone,
            'isAdministrator': True
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user_2.id}', user_admin_2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('Solo puede actualizar sus datos, no puede actualizar información ajena', response.data['message'])
        self.assertEqual(len(response.data), 1)


        user_admin_3 = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email,
            'telephone': self.user.telephone,
            'isAdministrator': False
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.admin.id}', user_admin_3)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('Solo puede actualizar sus datos, no puede actualizar información ajena', response.data['message'])
        self.assertEqual(len(response.data), 1)



        user_active = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email,
            'telephone': self.user.telephone,
            'isActive': False
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user_2.id}', user_active)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('Solo puede actualizar sus datos, no puede actualizar información ajena', response.data['message'])
        self.assertEqual(len(response.data), 1)


        user_active_2 = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email,
            'telephone': self.user.telephone,
            'isActive': False
        }

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.admin.id}', user_active_2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('Solo puede actualizar sus datos, no puede actualizar información ajena', response.data['message'])
        self.assertEqual(len(response.data), 1)



    
    def test_positive_update(self):
        fake = Faker('es_ES')

        user = {
            'dni': '29874526P',
            'name': 'Nombre actualizado',
            'surname': 'Apellido nuevo',
            'username': 'usuarioPUT',
            'password': 'contraseña.put',
            'email': 'nuevoemail@hotmail.com',
            'telephone': '+34678091235',
            
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.put(f'/users/{self.user.id}', user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



        user_admin = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': self.user.surname,
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email,
            'telephone': self.user.telephone,
            'isAdministrator': True

        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.put(f'/users/{self.user_2.id}', user_admin)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



        user_admin_2 = {
            'dni': self.user.dni,
            'name': self.user.name,
            'surname': 'Surname Updated',
            'username': self.user.username,
            'password': self.user.password,
            'email': self.user.email,
            'telephone': self.user.telephone,

        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.put(f'/users/{self.user_2.id}', user_admin_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    ### DELETE

    def test_negative_delete(self):
        response = self.client.delete(f'/users/{self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.delete(f'/users/{self.admin.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.delete(f'/users/{self.user_2.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.delete(f'/users/{self.user_2.id+10}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_positive_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.delete(f'/users/{self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.delete(f'/users/{self.user_2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_admin)
        response = self.client.delete(f'/users/{self.admin.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)