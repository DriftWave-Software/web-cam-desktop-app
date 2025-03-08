from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import cv2
import numpy as np
from PIL import Image
import io
import os
from django.conf import settings
import time
import re

def index(request):
    return render(request, 'camera/index.html')

@csrf_exempt
def capture(request):
    if request.method == 'POST':
        try:
            # Get the image data from the POST request
            image_data = request.POST.get('image')
            if not image_data:
                return JsonResponse({'error': 'No image data received'}, status=400)

            # Extract the base64 data after the comma
            image_data = re.sub('^data:image/.+;base64,', '', image_data)
            
            # Decode base64 string
            image_bytes = base64.b64decode(image_data)
            
            # Create a BytesIO object for PIL
            image_buffer = io.BytesIO(image_bytes)
            
            # Open the image with PIL
            image = Image.open(image_buffer)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Create media directory if it doesn't exist
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            
            # Save the image
            timestamp = int(time.time())
            filename = f'selfie_{timestamp}.jpg'
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            
            # Save as JPEG for better compatibility
            image.save(file_path, 'JPEG', quality=95)
            
            return JsonResponse({
                'success': True,
                'message': 'Image captured successfully',
                'image_url': f'{settings.MEDIA_URL}{filename}'
            })
            
        except Exception as e:
            import traceback
            print("Error details:", traceback.format_exc())  # Print detailed error
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)
