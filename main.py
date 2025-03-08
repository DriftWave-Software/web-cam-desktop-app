import webview
import sys
import os
import subprocess
import time
import signal
import atexit
from django.core.wsgi import get_wsgi_application

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selfie_booth.settings')

def start_django():
    # Start Django server as a separate process
    django_process = subprocess.Popen(['python', 'manage.py', 'runserver', '8000'])
    
    # Register cleanup function
    def cleanup():
        django_process.terminate()
        django_process.wait()
    
    atexit.register(cleanup)
    
    # Wait for Django to start
    time.sleep(2)
    return django_process

if __name__ == '__main__':
    # Start Django server
    django_process = start_django()
    
    try:
        # Create a desktop window
        window = webview.create_window('Selfie Booth', 'http://localhost:8000',
                                     width=800, height=600,
                                     resizable=True,
                                     fullscreen=False)
        webview.start()
    finally:
        # Cleanup Django process
        django_process.terminate()
        django_process.wait()
