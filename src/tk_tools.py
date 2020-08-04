import tkinter as tk
from PIL import Image, ImageTk


class TkTools:

    @classmethod
    def get_image_tk(cls, image_file):
        if not(cls.is_image_file_valid(image_file)):
            raise tk.TclError("Error: Invalid image file")

        return ImageTk.PhotoImage(Image.open(image_file))

    @classmethod
    def get_image_tk_resized(cls, image_file, width, height):
        if not(cls.is_image_file_valid(image_file)):
            raise tk.TclError("Error: Invalid image file")

        if type(width) != int or type(height) != int:
            raise tk.TclError("Error: Invalid width and height values")
        
        img = Image.open(image_file)
        img = img.resize((width, height), Image.ANTIALIAS)
        image_tk = ImageTk.PhotoImage(img)
        return image_tk

    @staticmethod
    def is_image_file_valid(image_file):
        if image_file == None or image_file == "":
            return False

        try:
            Image.open(image_file)
            return True
        except:
            return False