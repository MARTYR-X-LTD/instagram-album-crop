import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2) # if your windows version >= 8.1
except:
    ctypes.windll.user32.SetProcessDPIAware() # win 8.0 or less 
from PIL import Image
import os
import sys
import subprocess
from tkinter import messagebox

class window_class:

    def __init__(self, master):
        self.master = master
        
        width_screen = self.master.winfo_screenwidth()
        height_screen = self.master.winfo_screenheight()
        dpi = self.master.winfo_fpixels('1i')
        scaling_factor = round(dpi / 96, 2)

        w_window = int(600 * scaling_factor)
        h_window = int(340 * scaling_factor)
        # padding
        w_window_p = int(40 * scaling_factor)
        h_window_p = int(40 * scaling_factor)


        self.save_same_folder = tk.IntVar(value=1)
        self.width_crop = tk.IntVar(value=1080)
        self.filename = self.file_dir = self.save_folder_custom = None

        self.master.title("Instagram Album Crop")
        
        # calculations to spawn window at the center
        width_spawn = int(width_screen/2 - w_window/2)
        height_spawn = int(height_screen/2 - h_window/2)
        # root.tk.call('tk', 'scaling', scaling_factor)
        self.master.geometry(f"{w_window}x{h_window}+{width_spawn}+{height_spawn}")
        self.master.resizable(False, False)

        main_frame = tk.Frame(self.master, highlightbackground="green", highlightcolor="green", highlightthickness=0)
        main_frame.pack(padx=w_window_p, pady=h_window_p, fill='both', expand=True)

        self.place_info = tk.Label(main_frame,text="↓ Place your Instagram album/carousel here")
        self.place_info.grid(column=0, row=0, columnspan=2, sticky='w')

        self.select_image_button = tk.Button(main_frame, text="Select Image", command=self.select_image, width=20)
        self.select_image_button.grid(column=0, row=1, padx=(0,10), pady=10, sticky="w")

        self.image_location = tk.Entry(main_frame)
        self.image_location.grid(column=1, row=1, columnspan=2, padx=10, pady=10, sticky="nswe")
        self.image_location.configure(state='readonly')

        self.same_folder_check = tk.Checkbutton(main_frame, text="Save slices in the same folder of the image", 
                                    variable=self.save_same_folder, command=lambda: self.display_save_folder())
        self.same_folder_check.grid(row=2, column=0, pady=(30,0), columnspan=2, sticky='w')

        self.save_folder_button = tk.Button(main_frame, text="Folder to save", command=self.select_save_folder, width=20)

        self.save_folder_entry = tk.Entry(main_frame)
        self.save_folder_entry.configure(state='readonly')

        self.width_crop_frame = tk.Frame(main_frame)
        self.width_crop_frame.grid(column=0, columnspan=2, row=5, pady=(10,0), sticky="nsw")

        self.width_crop_info = tk.Label(self.width_crop_frame,text="Width of slices in px")
        self.width_crop_info.grid(column=0, columnspan=2, row=0, sticky='sw')
        
        self.width_crop_entry = tk.Entry(self.width_crop_frame, textvariable=self.width_crop, width=5)
        self.width_crop_entry.grid(column=0, row=1, pady=(6,0), padx=(2,6), sticky="nsw")

        self.width_crop_default = tk.Label(self.width_crop_frame,text="Default: 1080")
        self.width_crop_default.grid(column=1, row=1, columnspan=2, sticky='sw')

        self.about_label = tk.Label(main_frame, text='About', fg="blue", cursor="hand2")
        self.about_label.grid(column=1, row=5, sticky="se", padx=(0,10))
        #self.about_label.bind("<Button-1>", command=lambda: self.display_save_folder())

        self.crop_button = tk.Button(main_frame, text="Crop", command=self.crop, width=15)
        self.crop_button.grid(column=2, row=5, sticky="se")
        self.crop_button.configure(state='disable')




        #main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)

    def display_save_folder(self):
        if self.save_same_folder.get(): # if this returns 1
            self.save_folder_button.grid_forget()
            self.save_folder_entry.grid_forget()
        else:
            self.save_folder_button.grid(column=0, row=3, padx=(0,10), pady=10, sticky="w")
            self.save_folder_entry.grid(column=1, row=3, columnspan=2, padx=10, pady=10, sticky="nswe")

    def select_image(self):
        ftypes = [('Image Files', ['*.jpg', '*.png'])]
        image_dialog = filedialog.askopenfilename(filetypes = ftypes, title = "Select the Instagram album image to be cropped")
        if not image_dialog:
            return
        self.image_to_crop = image_dialog
        filename_and_ext = os.path.basename(self.image_to_crop)
        self.filename = os.path.splitext(filename_and_ext)[0]
        self.file_dir = os.path.dirname(os.path.realpath(self.image_to_crop))

        self.image_location.configure(state='normal')
        self.image_location.delete(0, 'end')
        self.image_location.insert(0, self.image_to_crop.replace('/', os.sep)) # this mess to fix visually the forward slashes
        self.image_location.xview_moveto(1)
        self.image_location.configure(state='readonly')

        if not self.save_folder_custom:
            self.save_folder_entry.configure(state='normal')
            self.save_folder_entry.delete(0, 'end')
            self.save_folder_entry.insert(0, self.file_dir)
            self.save_folder_entry.xview_moveto(1)
            self.save_folder_entry.configure(state='readonly')

        self.crop_button.configure(state='active')
        return

    def select_save_folder(self):
        save_folder_dialog = filedialog.askdirectory(title = "Select the Instagram album image to be cropped")
        if not save_folder_dialog:
            return
        self.save_folder_custom = save_folder_dialog
        self.save_folder_entry.configure(state='normal')
        self.save_folder_entry.delete(0, 'end')
        self.save_folder_entry.insert(0, self.save_folder_custom.replace('/', os.sep))
        self.save_folder_entry.xview_moveto(1)
        self.save_folder_entry.configure(state='readonly')

    def crop(self):
        self.crop_button.configure(state='disable', text="Cropping...")
        try:
            im = Image.open(self.image_to_crop)
        except:
            messagebox.showinfo(title="Error", message="Can't open the file")
            self.crop_button.configure(state='enable', text="Crop")
            return

        width_im, height_im = im.size

        number_crops = width_im/self.width_crop.get()


        # add one more crop for images that are not multiple of the slice width. Will result in the last image being
        # smaller in width of course
        if (number_crops % 1) != 0:
            number_crops += 1.0


        top = 0
        bottom = height_im

        if self.save_same_folder.get() == 1 or self.save_folder_custom == None:
            save_folder = self.file_dir
        else:
            save_folder = self.save_folder_custom.replace('/', os.sep)


        for i in range(int(number_crops)):
            left = i*1080
            right = (i+1)*1080

            # for images that are not multiple of the slice width.
            if right > width_im:
                right = width_im

            temp_crop = im.crop((left, top, right, bottom)) 
            temp_crop.save(f'{save_folder}{os.sep}{self.filename}_crop_ig-{str(i+1)}.jpg', quality=100, subsampling=0)

        self.crop_button.configure(state='active', text="Crop")
        if sys.platform == 'darwin':
            subprocess.call(['open', '--', save_folder])
        elif sys.platform == 'win32':
            subprocess.call(['explorer', save_folder])



def main(): 
    root = tk.Tk()
    app = window_class(root)
    root.mainloop()

main()
