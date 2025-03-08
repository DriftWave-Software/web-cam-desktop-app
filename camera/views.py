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

            # Remove the data URL prefix
            image_data = image_data.replace('data:image/png;base64,', '')
            
            # Convert base64 to image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Save the image
            timestamp = int(time.time())
            filename = f'selfie_{timestamp}.png'
            save_path = os.path.join(settings.MEDIA_ROOT, filename)
            
            # Create the media directory if it doesn't exist
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            
            # Save the image
            image.save(save_path, 'PNG')
            
            return JsonResponse({
                'success': True,
                'message': 'Image captured successfully',
                'image_url': f'{settings.MEDIA_URL}{filename}'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)
