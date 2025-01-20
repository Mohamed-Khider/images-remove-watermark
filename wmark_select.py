import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np


def advanced_remove_watermark(image_path, output_path):
    """Remove watermark using advanced inpainting techniques."""
    image = cv2.imread(image_path)
    if image is None:
        messagebox.showerror("Error", "Invalid image file.")
        return False

    clone = image.copy()
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    def draw_mask(event, x, y, flags, param):
        """Allow user to draw the mask interactively."""
        nonlocal drawing
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                cv2.circle(mask, (x, y), 10, 255, -1)
                cv2.circle(image, (x, y), 10, (0, 0, 255), -1)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False

    # OpenCV window for mask drawing
    drawing = False
    cv2.namedWindow("Draw Mask")
    cv2.setMouseCallback("Draw Mask", draw_mask)

    while True:
        cv2.imshow("Draw Mask", image)
        key = cv2.waitKey(1) & 0xFF
        if key == 13:  # Enter to confirm
            break
        elif key == 27:  # Esc to cancel
            cv2.destroyAllWindows()
            return False

    cv2.destroyAllWindows()

    # Perform inpainting
    result = cv2.inpaint(clone, mask, 7, cv2.INPAINT_TELEA)

    # Save the result
    cv2.imwrite(output_path, result)
    return True


def open_image():
    """Open an image file dialog."""
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((400, 400))  # Resize for display
        photo = ImageTk.PhotoImage(img)
        panel.configure(image=photo)
        panel.image = photo

        global current_image_path
        current_image_path = file_path


def process_image():
    """Process the current image to remove watermark."""
    if not current_image_path:
        messagebox.showerror("Error", "No image selected.")
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
    if not output_path:
        return

    success = advanced_remove_watermark(current_image_path, output_path)
    if success:
        messagebox.showinfo("Success", f"Watermark removed and saved to {output_path}")


# GUI
root = tk.Tk()
root.title("Professional Watermark Remover")

panel = tk.Label(root)
panel.pack(pady=10)

btn_open = tk.Button(root, text="Open Image", command=open_image)
btn_open.pack(pady=5)

btn_process = tk.Button(root, text="Remove Watermark", command=process_image)
btn_process.pack(pady=5)

current_image_path = None

root.mainloop()
