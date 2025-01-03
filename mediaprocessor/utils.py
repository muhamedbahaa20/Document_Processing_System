from django.core.files.base import ContentFile
from PIL import Image
import base64
import fitz 

def save_base64_file(data, file_name):
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]
    file_data = ContentFile(base64.b64decode(imgstr), name=f"{file_name}.{ext}")
    return file_data

def get_image_details(file_path,file_name):
    with Image.open(file_path) as img:
        return {
            "name": file_name,
            "location": file_path,
            "width": img.width,
            "height": img.height,
            "channels": len(img.getbands()),
        }

def get_pdf_details(file_path,file_name):
    pdf = fitz.open(file_path)
    page = pdf[0]
    return {
        "name": file_name,
        "location": file_path,
        "number_of_pages": len(pdf),
        "page_width": page.rect.width,
        "page_height": page.rect.height,
    }