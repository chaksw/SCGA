from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from .models import Scga
# Create your tests here.


class SCGAModelTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/scgas/'

    def test_create_model_with_pkl_file(self):
        # create a
        pass
