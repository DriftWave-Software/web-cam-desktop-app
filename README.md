# Camera Application

A desktop application built with Python that allows you to capture images using your camera with various features:

## Features
- Live camera preview
- Timer functionality (0-10 seconds)
- Real-time filters (none, grayscale, blur, sepia)
- Image saving with timestamp
- Support for built-in cameras, webcams, and USB cameras

## Requirements
- Python 3.x
- OpenCV
- Pillow
- NumPy

## Installation
1. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage
1. Run the application:
```bash
python camera_app.py
```

2. The application will open with a live camera preview
3. Select a filter from the dropdown menu (optional)
4. Set a timer duration (0-10 seconds)
5. Click "Capture" to take a photo
6. Images are saved in the "images" directory with timestamps

## Notes
- The application will automatically use the default camera (index 0)
- To use a different camera, modify the camera index in the code
- Captured images are saved in the "images" directory
