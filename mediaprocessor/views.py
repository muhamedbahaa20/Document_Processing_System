from io import BytesIO
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.conf import settings
import os
from .models import UploadedFile
from .serializers import UploadedFileSerializer
from .utils import save_base64_file, get_image_details, get_pdf_details
import fitz 
from PIL import Image
from django.http import FileResponse

@api_view(['POST'])
def convert_pdf_to_image(request):
    try:
        file_id = request.data['id']
        file = UploadedFile.objects.get(pk=file_id, file_type='pdf')

        pdf = fitz.open(file.file.path)
        page = pdf[0]
        pix = page.get_pixmap()
        img_path = file.file.path.replace('.pdf', '.png')
        pix.save(img_path)

        new_file = UploadedFile.objects.create(file=img_path, file_type='image',file_name=file.file_name)
        serializer = UploadedFileSerializer(new_file)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def upload_file(request):
    try:
        data = request.data
        file_data = save_base64_file(data['file'], data['name'])
        file_type = data['type']

        uploaded_file = UploadedFile.objects.create(file=file_data, file_type=file_type, file_name = data['name'])
        serializer = UploadedFileSerializer(uploaded_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_files(request, file_type):
    files = UploadedFile.objects.filter(file_type=file_type)
    serializer = UploadedFileSerializer(files, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_file_details(request, file_type, pk):
    try:
        file = UploadedFile.objects.get(pk=pk, file_type=file_type)
        file_path = file.file.path

        if file_type == 'image':
            details = get_image_details(file_path,file.file_name)
        elif file_type == 'pdf':
            details = get_pdf_details(file_path,file.file_name)
        else:
            return Response({"error": "Invalid file type"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(details)
    except UploadedFile.DoesNotExist:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_file(request, file_type, pk):
    try:
        file = UploadedFile.objects.get(pk=pk, file_type=file_type)
        file_path = file.file.path
        file.delete()
        if os.path.exists(file_path):
            os.remove(file_path)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except UploadedFile.DoesNotExist:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def rotate_image(request):
    try:
        file_id = request.data['id']
        angle = request.data['angle']
        file = UploadedFile.objects.get(pk=file_id, file_type='image')

        with Image.open(file.file.path) as img:
            rotated_img = img.rotate(angle, expand=True)
            rotated_img.save(file.file.path)
            buffer = BytesIO()
            rotated_img.save(buffer, format=img.format)
            buffer.seek(0)

        return FileResponse(buffer, as_attachment=False, content_type=f"image/{img.format.lower()}")
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



# class ConvertPdfToImageView(APIView):
#     def post(self, request):
#         try:
#             file_id = request.data['id']
#             file = UploadedFile.objects.get(pk=file_id, file_type='pdf')

#             # Open the PDF and convert the first page to an image
#             pdf = fitz.open(file.file.path)
#             page = pdf[0]  # Get the first page of the PDF
#             pix = page.get_pixmap()  # Convert page to pixmap (image)
#             img_path = file.file.path.replace('.pdf', '.png')  # Save as PNG
#             pix.save(img_path)

#             # Create a new UploadedFile object for the image
#             new_file = UploadedFile.objects.create(file=img_path, file_type='image')

#             # Serialize the new file and return the response
#             serializer = UploadedFileSerializer(new_file)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)