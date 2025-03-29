from django.core.validators import ValidationError
from PIL import Image
from django.apps import apps

def validate_image_size(image):
    file_size = image.size
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f'ფაილი არ უნდა აღემატებოდეს {limit_mb}MB-ს')
    
def validate_image_resolution(image):
    img = Image.open(image)
    min_width, min_height = 300,300
    max_width, max_height = 4000,4000

    width, height = image.size

    if width < min_width or height < min_height:
        raise ValidationError(f'სურათი ძალიან პატარაა. მინიმალური ზომაა {min_width} X {min_height}პიქსელი')
    
    if width > max_width or height > max_height:
        raise ValidationError(f'სურათი ძალიან დიდია. მაქსიმალური ზომაა {min_width} X {min_height}პიქსელი')
    

def validate_image_count(product_id):
    ProductImage = apps.get_model('products', 'ProductImage')
    max_images = 5
    if ProductImage.objects.filter(product_id=product_id).count() >= max_images:
        raise ValidationError(f'პროდუქტს უკვე აქვს მაქსიმალური რაოდენობის სურათები')
    
    