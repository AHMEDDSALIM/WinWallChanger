import ctypes
import os
import winreg
import customtkinter as ctk
from tkinter import filedialog, messagebox
import sys
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Function to set lock screen image
def set_lock_screen_image(image_path):
    try:
        if not os.path.exists(image_path):
            return False

        reg_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\PersonalizationCSP"
        reg_name = "LockScreenImagePath"
        
        with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_key) as key:
            winreg.SetValueEx(key, reg_name, 0, winreg.REG_SZ, image_path)

        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        return True
    except PermissionError:
        messagebox.showinfo("Error", "You need to run this app as administrator to work correctly.", icon="error")

        return False
    except Exception as e:
        return False

# Function to set desktop wallpaper
def set_desktop_wallpaper(image_path):
    try:
        if not os.path.exists(image_path):
            messagebox.showinfo("Error", "Image file does not exist.")
            return False

        SPI_SETDESKWALLPAPER = 20
        success = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

        if success:
            return True
        else:
            return False
    except Exception as e:
        return False

# Function to select an image
def select_image():
    image_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if image_path:
        # Update lock screen and desktop wallpaper
        image_path = image_path.replace("/", "\\")
        lock_screen_success = set_lock_screen_image(image_path)
        desktop_success = set_desktop_wallpaper(image_path)

        if lock_screen_success and desktop_success:
            status_label.configure(text="Lock screen and desktop wallpaper updated successfully.", text_color="green")
            app.after(2000, lambda: status_label.configure(text="Click the button below to select an image.",text_color="normal"))
        else:
            messagebox.showerror("Error", "Failed to update lock screen or desktop wallpaper.")
    else:
        messagebox.showwarning("No File Selected", "Please select an image file.")
# CustomTkinter App UI
ctk.set_appearance_mode("light")
app = ctk.CTk()
app.geometry("400x150")
app.title("WinWallchanger")
app.iconbitmap(resource_path("assets/WinWallchangericon.ico"))
app.resizable(False, False)

# Add a button to select image
status_label = ctk.CTkLabel(app, text="Click the button below to select an image.") 
status_label.pack(pady=20)
select_button = ctk.CTkButton(app, text="Select Image", command=select_image)
select_button.pack(pady=20)

# Run the app
app.mainloop()
