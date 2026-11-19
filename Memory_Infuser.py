import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
from glitch_this import ImageGlitcher
from datetime import datetime
import hashlib
import os
import string
import threading
import time

# Glitch function
def glitch_jpeg_file(filename, text_snippet):
    glitcher = ImageGlitcher()
    text_hash = hashlib.md5(text_snippet.encode()).hexdigest()
    seed = int(text_hash, 16) % (10 ** 8)

    intensity = 0
    for char in text_snippet:
        if char.isdigit():
            intensity += 1
        elif char.islower():
            intensity += 2
        elif char.isupper():
            intensity += 3
        elif char in string.punctuation:
            intensity += 4

    intensity = 1 + (intensity % 10)
    glitch_img = glitcher.glitch_image(filename, intensity, color_offset=True, seed=seed)
    
    text_layer = Image.new('RGBA', glitch_img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_layer)
    width, height = glitch_img.size
    font = ImageFont.truetype("arial.ttf", 70)
    y_text = 0
    lines = text_snippet.splitlines()
    for line in lines:
        words = line.split()
        new_line = ""
        for word in words:
            if draw.textbbox((0, 0), new_line + word, font=font)[2] <= width:
                new_line += word + " "
            else:
                draw.text((10, y_text), new_line, font=font, fill=(255, 255, 255, 48))
                y_text += font.getbbox(new_line)[3] - font.getbbox(new_line)[1]
                new_line = word + " "
        draw.text((10, y_text), new_line, font=font, fill=(255, 255, 255, 48))
        y_text += font.getbbox(new_line)[3]

    glitch_img = Image.alpha_composite(glitch_img.convert('RGBA'), text_layer)
    glitch_img = glitch_img.convert('RGB')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")[:-4]
    glitched_filename = f'{filename.replace(".jpg", "")}_glitched_{timestamp}.jpg'
    glitch_img.save(glitched_filename)

    return glitched_filename

def load_image(filename):
    img = Image.open(filename)
    img = ImageTk.PhotoImage(img)
    img_label.config(image=img)
    img_label.image = img

def open_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    if not filename_path:
        return
    load_original_image(filename_path)

def load_original_image(filename):
    img = Image.open(filename)
    img = ImageTk.PhotoImage(img)
    img_label.config(image=img)
    img_label.image = img

def update_image(event=None):  
    text_snippet = text_entry.get("1.0", "end-1c")
    glitched_filename = glitch_jpeg_file(filename_path, text_snippet)
    load_image(glitched_filename)
    return glitched_filename

def animate_text(event=None):  
    global animating, animation_thread
    if animating:
        return  

    text_snippet = text_entry.get("1.0", "end-1c")
    text_entry.delete("1.0", tk.END)

    animation_thread = threading.Thread(target=run_animation, args=(text_snippet,))
    animation_thread.start()

def run_animation(text_snippet):
    global animating
    animating = True

    for i in range(min(len(text_snippet), 300)):
        text_entry.insert(tk.END, text_snippet[i])
        update_image()
        time.sleep(0.2)

    animating = False

root = tk.Tk()
root.configure(bg='black')

open_file_button = tk.Button(root, text='Open File', command=open_file, bg='black', fg='white', font=("Courier", 14))
open_file_button.pack()

text_label = tk.Label(root, text='Insert Memory', bg='black', fg='white', font=("Courier", 14))
text_label.pack()
text_entry = tk.Text(root, bg='black', fg='white', insertbackground='white', font=("Courier", 14), height=5)
text_entry.pack()
text_entry.bind("<Return>", animate_text)

glitch_button = tk.Button(root, text='Infuse Memory', command=animate_text, bg='black', fg='white', font=("Courier", 14))
glitch_button.pack()

img_label = tk.Label(root, bg='black')
img_label.pack()

animating = False
animation_thread = None
filename_path = None

root.mainloop()
