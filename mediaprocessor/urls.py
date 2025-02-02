from django.urls import path
from .views import upload_file, list_files, get_file_details, delete_file, rotate_image,convert_pdf_to_image

urlpatterns = [
    path('api/upload/', upload_file,name='upload_file'),
    path('api/<str:file_type>/', list_files,name='list_files'),
    path('api/<str:file_type>/<int:pk>/', get_file_details,name='get_file_details'),
    path('api/<str:file_type>/<int:pk>/delete/', delete_file,name='delete_file'),
    path('api_rotate/', rotate_image,name='rotate_image'),
    path('api/', convert_pdf_to_image,name='convert_pdf_to_image'),
]