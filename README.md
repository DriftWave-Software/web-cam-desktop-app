# Selfie Booth Desktop Application

A cross-platform desktop selfie booth application built with Django and PyWebView. This application allows users to take selfies using their computer's built-in camera and save them locally.

## Features

- Live camera preview
- Capture photos with a single click
- Cross-platform support (Windows & Mac)
- Modern and intuitive user interface
- Local storage of captured images

## Prerequisites

### System Dependencies (Linux/Ubuntu)

```bash
sudo apt-get update
sudo apt-get install -y \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-3.0 \
    gir1.2-webkit2-4.0 \
    libgirepository1.0-dev \
    gcc \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    libwebkit2gtk-4.0-dev
```

### For Windows
- Python 3.8 or higher
- Microsoft Visual C++ 14.0 or higher

### For macOS
```bash
brew install python-tk webkit2png
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd django-desktop-app
```

2. Create and activate a Python virtual environment:
```bash
# Using pyenv
pyenv virtualenv 3.11.0 photobooth
pyenv activate photobooth

# Or using regular venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python manage.py migrate
```

## Running the Application

1. Start the application:
```bash
python main.py
```

2. The application will open in a desktop window showing the camera preview.

3. Click the "Take Photo" button to capture a selfie.

4. Captured photos are saved in the `media` directory.

## Project Structure

```
django-desktop-app/
├── main.py              # Main application entry point
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── static/            # Static files directory
├── media/             # Saved photos directory
├── selfie_booth/      # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── camera/            # Camera handling app
    ├── views.py
    ├── urls.py
    └── templates/
        └── camera/
            └── index.html
```

## Troubleshooting

### Linux
- If you get GTK/WebKit errors, make sure all system dependencies are installed:
```bash
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0
```

### Windows
- If you get webcam access errors, make sure your camera is enabled in Windows settings
- Install Visual C++ Build Tools if you get compilation errors

### macOS
- Allow camera access when prompted
- If WebKit is not found, reinstall it using brew:
```bash
brew reinstall webkit2png
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
