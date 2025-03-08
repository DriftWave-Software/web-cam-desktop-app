import cv2
import numpy as np
from datetime import datetime
import os
from PIL import Image

class SelfieBooth:
    def __init__(self):
        self.setup_camera()
        self.create_media_dir()
        
    def setup_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Could not open camera")
            
        # Set camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
    def create_media_dir(self):
        os.makedirs('media', exist_ok=True)
        
    def capture_photo(self):
        ret, frame = self.cap.read()
        if ret:
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'media/selfie_{timestamp}.jpg'
            
            # Convert BGR to RGB for PIL
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            image.save(filename, 'JPEG', quality=95)
            
            # Show "Captured!" text on preview
            preview = frame.copy()
            cv2.putText(preview, 'Captured!', (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Selfie Booth', preview)
            cv2.waitKey(1000)  # Show "Captured!" for 1 second
            
            return filename
        return None
        
    def run(self):
        cv2.namedWindow('Selfie Booth', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Selfie Booth', 800, 600)
        
        print("Press SPACE to take a photo")
        print("Press Q to quit")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Show instructions on frame
            cv2.putText(frame, 'SPACE: Capture  Q: Quit', (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Display the frame
            cv2.imshow('Selfie Booth', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):  # Space key
                filename = self.capture_photo()
                if filename:
                    print(f"Photo saved as: {filename}")
        
        # Clean up
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        booth = SelfieBooth()
        booth.run()
    except Exception as e:
        print(f"Error: {e}")
