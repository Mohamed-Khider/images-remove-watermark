import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np


def remove_watermark(image_path, output_path):
    """Remove watermark from the given image using OpenCV inpainting."""
    image = cv2.imread(image_path)
    if image is None:
        messagebox.showerror("Error", "Invalid image file.")
        return False

    # Let user create a mask interactively using OpenCV window
    mask = cv2.inRange(image, (200, 200, 200), (255, 255, 255))  # Adjust for watermark color
    result = cv2.inpaint(image, mask, 7, cv2.INPAINT_TELEA)

    cv2.imwrite(output_path, result)
    return True


def open_image():
    """Open an image file dialog."""
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])
    if file_path:
        # Load and display the image in the GUI
        img = Image.open(file_path)
        img.thumbnail((400, 400))  # Resize for display
        photo = ImageTk.PhotoImage(img)
        panel.configure(image=photo)
        panel.image = photo

        # Save path to use later
        global current_image_path
        current_image_path = file_path


def process_image():
    """Process the current image to remove watermark."""
    if not current_image_path:
        messagebox.showerror("Error", "No image selected.")
        return

    # Define output file
    output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
    if not output_path:
        return

    # Remove watermark
    success = remove_watermark(current_image_path, output_path)
    if success:
        messagebox.showinfo("Success", f"Watermark removed and saved to {output_path}")


# Create the GUI
root = tk.Tk()
root.title("Watermark Remover")

# UI Components
panel = tk.Label(root)
panel.pack(pady=10)


btn_open = tk.Button(root, text="Open Image", command=open_image)
btn_open.pack(pady=5)

btn_process = tk.Button(root, text="Remove Watermark", command=process_image)
btn_process.pack(pady=5)

# Global variable to store the current image path
current_image_path = None

# Run the application
root.mainloop()
