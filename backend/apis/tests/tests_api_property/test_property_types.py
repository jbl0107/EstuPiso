from rest_framework import status
from rest_framework.test import APITestCase

from django.conf import settings



class TestPropertyTypes(APITestCase):

    
    def setUp(self):
        pass


    def test_positive(self):
        response = self.client.get(f'/properties/types')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ["Inmueble completo", "Habitacion",  "Cama"])


