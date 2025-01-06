import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from .models import UploadedFile


@pytest.mark.django_db
def test_list_files():
    client = APIClient()
    UploadedFile.objects.create(file='uploads/test.pdf', file_type='pdf', file_name='test.pdf')
    
    response = client.get(reverse('list_files', kwargs={'file_type': 'pdf'}))
    
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['file_name'] == 'test.pdf'

@pytest.mark.django_db
def test_get_file_details(sample_image_file):
    client = APIClient()
    uploaded_file = UploadedFile.objects.create(file='uploads/lecture11.png', file_type='image', file_name='lecture11.png')
    
    response = client.get(reverse('get_file_details', kwargs={'file_type': 'image', 'pk': uploaded_file.id}))
    
    assert response.status_code == 200
    assert 'width' in response.data  # Assuming `get_image_details` returns width
    assert 'height' in response.data

@pytest.mark.django_db
def test_delete_file():
    client = APIClient()
    uploaded_file = UploadedFile.objects.create(file='uploads/lecture1.pdf', file_type='pdf', file_name='lecture1.pdf')
    
    response = client.delete(reverse('delete_file', kwargs={'file_type': 'pdf', 'pk': uploaded_file.id}))
    
    assert response.status_code == 204
    assert UploadedFile.objects.count() == 0

