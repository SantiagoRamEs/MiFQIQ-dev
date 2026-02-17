import os
from django.core.exceptions import ValidationError
from PIL import Image

def validate_image_size(image):
    """Valida que la imagen no exceda 5MB"""
    file_size = image.file.size
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f'El archivo no puede exceder {limit_mb}MB')

def validate_image_format(image):
    """Valida que la imagen sea JPEG o PNG"""
    valid_formats = ['JPEG', 'PNG', 'JPG']
    try:
        img = Image.open(image)
        if img.format not in valid_formats:
            raise ValidationError('Por favor sube una imagen en formato JPEG o PNG')
    except Exception as e:
        raise ValidationError('El archivo no es una imagen válida')

def validate_image_dimensions(image, max_width=1920, max_height=1080):
    """Valida las dimensiones de la imagen"""
    try:
        img = Image.open(image)
        width, height = img.size
        if width > max_width or height > max_height:
            raise ValidationError(f'La imagen no puede ser mayor a {max_width}x{max_height} píxeles')
    except Exception as e:
        raise ValidationError('No se pudo validar las dimensiones de la imagen')
