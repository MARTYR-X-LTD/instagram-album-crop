import os
import sys
import subprocess
from PIL import Image

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import messagebox

# fix for high-dpi Windows systems. Exclude it from macOS builds.
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2) # if Windows version >= 8.1
except:
    ctypes.windll.user32.SetProcessDPIAware() # if Windows version <= 8.0


if sys.platform == 'darwin':
    s_pad = 4
    m_pad = 6
    l_pad = 20
    slice_entry_w = 4
    crop_button_w = 12
    normal_button_w = 12
elif sys.platform == 'win32':
    s_pad = 6
    m_pad = 10
    l_pad = 30
    slice_entry_w = 5
    crop_button_w = 15
    normal_button_w = 20


class window_class:
    def __init__(self, master):
        self.master = master
        
        width_screen = self.master.winfo_screenwidth()
        height_screen = self.master.winfo_screenheight()

        if sys.platform == 'darwin':
            scaling_factor = 1
        elif sys.platform == 'win32':
            dpi = self.master.winfo_fpixels('1i')
            scaling_factor = round(dpi / 96, 2)

        # size window
        w_window = int(600 * scaling_factor)
        h_window = int(340 * scaling_factor)
        # padding
        w_window_p = int(40 * scaling_factor)
        h_window_p = int(40 * scaling_factor)

        # vars
        self.save_same_folder = tk.IntVar(value=1) # default save in the same folder
        self.width_slices = tk.IntVar(value=1080) # 1080px is the default max width for slices in Instagram
        self.filename = self.file_dir = self.save_folder_custom = None # Initial variables declare

        self.master.title("Instagram Album Crop")
        
        # calculations to spawn window at the center
        width_spawn = int(width_screen/2 - w_window/2)
        height_spawn = int(height_screen/2 - h_window/2)

        self.master.geometry(f"{w_window}x{h_window}+{width_spawn}+{height_spawn}")
        self.master.resizable(False, False)

        main_frame = tk.Frame(self.master)
        main_frame.pack(padx=w_window_p, pady=h_window_p, fill='both', expand=True)


        self.place_info = tk.Label(main_frame,text="↓ Place your Instagram album/carousel here")
        self.place_info.grid(column=0, row=0, columnspan=2, sticky='w')

        ##### Select image
        self.select_image_button = tk.Button(main_frame, text="Select Image", command=self.select_image, width=normal_button_w)
        self.select_image_button.grid(column=0, row=1, padx=(0,m_pad), pady=m_pad, sticky="w")
        self.image_location = tk.Entry(main_frame)
        self.image_location.grid(column=1, row=1, columnspan=2, padx=m_pad, pady=m_pad, sticky="nswe")
        self.image_location.configure(state='readonly')

        ##### Same folder check
        self.same_folder_check = tk.Checkbutton(main_frame, text="Save slices in the same folder of the image", 
                                    variable=self.save_same_folder, command=lambda: self.display_save_folder())
        self.same_folder_check.grid(row=2, column=0, pady=(l_pad,0), columnspan=2, sticky='w')

        ##### Save folder (default hidden)
        self.save_folder_button = tk.Button(main_frame, text="Folder to save", command=self.select_save_folder, width=normal_button_w)
        self.save_folder_entry = tk.Entry(main_frame)
        self.save_folder_entry.configure(state='readonly')

        ##### Width slices
        self.width_slices_frame = tk.Frame(main_frame)
        self.width_slices_frame.grid(column=0, columnspan=2, row=5, pady=(m_pad,0), sticky="nsw")

        self.width_slices_info = tk.Label(self.width_slices_frame,text="Width of slices in px")
        self.width_slices_info.grid(column=0, columnspan=2, row=0, sticky='sw')
        
        self.width_slices_entry = tk.Entry(self.width_slices_frame, textvariable=self.width_slices, width=slice_entry_w)
        self.width_slices_entry.grid(column=0, row=1, pady=(s_pad,0), padx=(2,s_pad), sticky="nsw")

        self.width_slices_default = tk.Label(self.width_slices_frame,text="Default: 1080")
        self.width_slices_default.grid(column=1, row=1, columnspan=2, sticky='sw')


        ##### About and crop button
        self.about_label = tk.Label(main_frame, text='About', fg="blue", cursor="hand2")
        self.about_label.grid(column=1, row=5, sticky="se", padx=(0,m_pad))

        self.crop_button = tk.Button(main_frame, text="Crop", command=self.crop, width=crop_button_w)
        self.crop_button.grid(column=2, row=5, sticky="se")
        self.crop_button.configure(state='disable')


        # No idea but this keeps things separated and expanded properly
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)


    def display_save_folder(self):
        # if checkbox is checked
        if self.save_same_folder.get(): 
            self.save_folder_button.grid_forget()
            self.save_folder_entry.grid_forget()
        else: # if checkbox is unchecked                         
            self.save_folder_button.grid(column=0, row=3, padx=(0,m_pad), pady=m_pad, sticky="w")
            self.save_folder_entry.grid(column=1, row=3, columnspan=2, padx=m_pad, pady=m_pad, sticky="nswe")


    # function to update text entries
    def entry_update(self, entry, directory):
        entry.configure(state='normal')
        entry.delete(0, 'end')
        entry.insert(0, directory.replace('/', os.sep))
        entry.xview_moveto(1)
        entry.configure(state='readonly')


    def select_image(self):
        ftypes = [('Image Files', ['*.jpg', '*.png'])]
        image_dialog = filedialog.askopenfilename(filetypes = ftypes, title = "Select the Instagram album image to be cropped")
        if not image_dialog:
            return
        
        # fill variables declared in __init__
        self.image_to_crop = image_dialog
        filename_and_ext = os.path.basename(self.image_to_crop)
        self.filename = os.path.splitext(filename_and_ext)[0]
        self.file_dir = os.path.dirname(os.path.realpath(self.image_to_crop))

        # update entry
        self.entry_update(self.image_location, self.image_to_crop)

        # update save folder if a custom one has not been chosen
        if not self.save_folder_custom:
            self.entry_update(self.save_folder_entry, self.file_dir)

        self.crop_button.configure(state='active')
        return
        

    def select_save_folder(self):
        save_folder_dialog = filedialog.askdirectory(title = "Select the Instagram album image to be cropped")
        if not save_folder_dialog:
            return
        self.save_folder_custom = save_folder_dialog
        self.entry_update(self.save_folder_entry, self.save_folder_custom)

        

    def crop(self):    
        self.crop_button.configure(state='disable', text="Cropping...")
        
        # load image
        try:
            im = Image.open(self.image_to_crop)
        except:
            messagebox.showinfo(title="Error", message="Can't open the file")
            self.crop_button.configure(state='enable', text="Crop")
            return

        # calculate number of slices (float)
        width_im, height_im = im.size
        number_slices = width_im/self.width_slices.get()

        # add one more crop for images that are not multiple of the slice width
        # Will result in the last image being smaller in width of course
        if (number_slices % 1) != 0:
            number_slices += 1.0

        # set save_folder
        if self.save_same_folder.get() == 1 or self.save_folder_custom == None:
            save_folder = self.file_dir
        else:
            save_folder = self.save_folder_custom.replace('/', os.sep)

        # common coordinates to each slice        
        top = 0
        bottom = height_im

        for i in range(int(number_slices)):
            left = i * self.width_slices.get()
            right = (i+1) * self.width_slices.get()

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


root = tk.Tk()
window_class(root)
root.mainloop()