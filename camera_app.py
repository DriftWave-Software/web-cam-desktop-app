import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import numpy as np
from datetime import datetime
import os

total_photos = 4  # Number of photos needed for collage

class CameraApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Camera App")
        self.window.geometry("1200x800")
        self.filename_to_print=None
        self.camera = cv2.VideoCapture(0)
        self.current_filter = "none"
        self.timer_count = 0
        self.is_timer_running = False
        self.captured_images = []
        self.templates = self.load_templates("templates")  # Load templates from folder
        self.selected_template = None  # Currently selected template
        self.template_positions = {}  # Positions for images in the template

        # Ensure the "images" folder exists
        self.output_folder = "images"
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.create_widgets()
        self.update_video()

    def load_templates(self, template_folder):
        templates = {}
        for filename in os.listdir(template_folder):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                template_path = os.path.join(template_folder, filename)
                template_image = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
                templates[filename] = template_image
        return templates

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.video_label = ttk.Label(self.main_frame)
        self.video_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        controls_frame = ttk.Frame(self.main_frame)
        controls_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Label(controls_frame, text="Timer (seconds):").pack(side=tk.LEFT, padx=5)
        self.timer_var = tk.StringVar(value="3")
        timer_spinbox = ttk.Spinbox(controls_frame, from_=0, to=10, width=5, textvariable=self.timer_var)
        timer_spinbox.pack(side=tk.LEFT, padx=5)

        ttk.Label(controls_frame, text="Filter:").pack(side=tk.LEFT, padx=5)
        self.filter_var = tk.StringVar(value="none")
        filters = ["none", "grayscale", "blur", "sepia"]
        filter_menu = ttk.OptionMenu(controls_frame, self.filter_var, "none", *filters, command=self.change_filter)
        filter_menu.pack(side=tk.LEFT, padx=5)

        ttk.Label(controls_frame, text="Select Template:").pack(side=tk.LEFT, padx=5)
        self.template_var = tk.StringVar(value="Select Template")
        template_menu = ttk.OptionMenu(controls_frame, self.template_var, "Select Template", *self.templates.keys(), command=self.select_template)
        template_menu.pack(side=tk.LEFT, padx=5)

        self.capture_btn = ttk.Button(controls_frame, text="Capture", command=self.start_collage)
        self.capture_btn.pack(side=tk.LEFT, padx=20)

        self.timer_label = ttk.Label(controls_frame, text="")
        self.timer_label.pack(side=tk.LEFT, padx=5)

    def update_video(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = self.apply_filter(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = frame.resize((800, 600))
            self.photo = ImageTk.PhotoImage(image=frame)
            self.video_label.configure(image=self.photo)
        self.window.after(10, self.update_video)

    def apply_filter(self, frame):
        if self.current_filter == "grayscale":
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif self.current_filter == "blur":
            return cv2.GaussianBlur(frame, (15, 15), 0)
        elif self.current_filter == "sepia":
            kernel = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]])
            return cv2.transform(frame, kernel)
        return frame

    def change_filter(self, value):
        self.current_filter = value

    def select_template(self, value):
        self.selected_template = self.templates[value]
        self.template_positions = self.get_template_positions(value)  # Define positions for the selected template

    def get_template_positions(self, template_name):
        # Define positions for each template (x, y, width, height)
        if template_name == "Birthday Party.png":
            return [
                (798, 125, 874, 580),  # Position for image 1
                (135, 765, 495, 315),  # Position for image 2
                (668, 765, 483, 315),  # Position for image 3
                (1188, 765, 495, 315),  # Position for image 4
            ]
        elif template_name == "Launch Program.png":
            return [
                (798, 115, 871, 570),  # Position for image 1
                (128, 763, 472, 315),  # Position for image 2
                (665, 763, 472, 315),  # Position for image 3
                (1202, 763, 475, 312),  # Position for image 4
            ]
        else:
            return []

    def start_collage(self):
        if self.selected_template is None:  # Fix: Check if template is None
            self.timer_label.configure(text="Please select a template first!")
            return
        self.captured_images = []
        self.timer_count = int(self.timer_var.get())
        self.capture_next()

    def capture_next(self):
        if len(self.captured_images) < total_photos:
            if self.timer_count > 0:
                self.timer_label.configure(text=f"Capturing in {self.timer_count}...")
                self.timer_count -= 1
                self.window.after(1000, self.capture_next)
            else:
                ret, frame = self.camera.read()
                if ret:
                    frame = cv2.flip(frame, 1)
                    frame = self.apply_filter(frame)
                    self.captured_images.append(frame)
                self.timer_count = int(self.timer_var.get())
                self.capture_next()
        else:
            self.create_collage()

    def create_collage(self):
        if len(self.captured_images) != total_photos:
            return

        # Create a copy of the selected template
        collage = self.selected_template.copy()

        # Resize and place each captured image on the template
        for i, (x, y, w, h) in enumerate(self.template_positions):
            if i < len(self.captured_images):
                resized_image = cv2.resize(self.captured_images[i], (w, h))

                # If the collage has 4 channels (RGBA), convert resized_image to 4 channels
                if collage.shape[2] == 4:
                    # Add an alpha channel to resized_image (fully opaque)
                    resized_image = cv2.cvtColor(resized_image, cv2.COLOR_RGB2RGBA)

                # Blend the resized_image into the collage
                collage[y:y+h, x:x+w] = resized_image

        # Save collage to the "images" folder
        filename = os.path.join(self.output_folder, f"collage_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        cv2.imwrite(filename, collage)

        # Convert to RGB format for Tkinter
        if collage.shape[2] == 4:  # If RGBA, convert to RGB
            collage_rgb = cv2.cvtColor(collage, cv2.COLOR_RGBA2RGB)
        else:
            collage_rgb = collage

        collage_pil = Image.fromarray(collage_rgb)
        collage_pil = collage_pil.resize((800, 600))  # Resize for display

        # Store in instance variable to prevent garbage collection
        self.collage_image = ImageTk.PhotoImage(collage_pil)

        # Update video label with the collage
        self.video_label.configure(image=self.collage_image)
        self.video_label.image = self.collage_image  # Prevent garbage collection
        self.timer_label.configure(text=f"Collage saved to {filename}! Displaying...")
        self.filename_to_print=filename
        # Add Print Button
        if not hasattr(self, "print_button"):  # Avoid multiple buttons
            self.print_button = ttk.Button(self.main_frame, text="Print", command=lambda: self.print_collage())
            self.print_button.grid(row=2, column=0, columnspan=2, pady=10)

    def print_collage(self):
        os.startfile(self.filename_to_print, "print")

    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()