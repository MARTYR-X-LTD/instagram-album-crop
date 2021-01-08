import sys
import random
import os
import subprocess
import webbrowser
import threading
import multiprocessing as mp
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton, QCheckBox, QSpacerItem, QFormLayout, QVBoxLayout,
                               QHBoxLayout, QWidget, QLineEdit, QGridLayout, QSizePolicy, QGroupBox, QFileDialog,
                               QMessageBox)
from PySide2.QtCore import Slot, Qt, Signal, QObject
from PySide2.QtGui import QIntValidator, QIcon

from PIL import Image
#os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
#os.environ["QT_SCALE_FACTOR"] = "1.5"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def crop_process(i, im, top, bottom, width_slices, width_im, save_folder, filename, extension):
    left = i * width_slices
    right = (i+1) * width_slices

    # for images that are not multiple of the slice width.
    if right > width_im:
        right = width_im

    temp_crop = im.crop((left, top, right, bottom))
    temp_crop.save(f'{save_folder}{os.sep}{filename}_crop_ig-{str(i+1)}{extension}', quality=100, subsampling=0)

class CropSignals(QObject):
    crop_started = Signal()
    crop_finished = Signal()
    crop_error = Signal()

class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("Instagram Album Cropper")
        self.setWindowIcon(QIcon(resource_path('icons/icon.ico')))

        # vars
        #self.save_same_folder = tk.IntVar(value=1) # default save in the same folder
        #self.width_slices = 1080 # 1080px is the default max width for slices in Instagram
        self.filename = self.extension = self.file_dir = self.save_folder_custom = None # Initial variables declare
       

        # Set main vertical layout for window
        grid = QVBoxLayout()

        # set GUI sizes for platform specific. Windows and Linux shared
        if sys.platform == 'darwin':
            grid.setContentsMargins(20,20,20,20)
            button_size = (100, 40)
            entry_h = 31
            bottom_button_size = (80, 40)
            slices_entry_width = 37
            spacer_same_folder = (0, 2)
            spacer_bottom = (0, 6)

            grid.setSpacing(10)

        else:
            grid.setContentsMargins(24,24,24,24)
            button_size = (100, 24)
            entry_h = 24
            bottom_button_size = (65, 24)
            slices_entry_width = 32
            spacer_same_folder = (0, 6)
            spacer_bottom = (0, 20)

        # Select image layout
        select_image_l = QHBoxLayout()

        select_image_button = QPushButton("🖼 Select Image")
        select_image_button.setMinimumSize(*button_size)
        select_image_button.clicked.connect(self.select_image)

        self.image_location = QLineEdit()
        self.image_location.setMinimumHeight(entry_h)
        self.image_location.setReadOnly(True)

        select_image_l.addWidget(select_image_button)
        select_image_l.addWidget(self.image_location)
        grid.addLayout(select_image_l)

        
        # Save folder layout
        save_folder_l = QHBoxLayout()
        
        save_folder_button = QPushButton("📁 Folder to save")
        save_folder_button.setMinimumSize(*button_size)
        save_folder_button.clicked.connect(self.select_save_folder)
        self.save_folder_entry = QLineEdit()
        self.save_folder_entry.setMinimumHeight(entry_h)
        self.save_folder_entry.setReadOnly(True)
        
        self.save_folder_check = QCheckBox("Save slices in the same folder of the image")
        self.save_folder_check.toggled.connect(save_folder_button.setDisabled)
        self.save_folder_check.toggled.connect(self.save_folder_entry.setDisabled)
        self.save_folder_check.setChecked(True)

        grid.addSpacerItem(QSpacerItem(*spacer_same_folder))

        grid.addWidget(self.save_folder_check)
        save_folder_l.addWidget(save_folder_button)
        save_folder_l.addWidget(self.save_folder_entry)
        grid.addLayout(save_folder_l)

        grid.addSpacerItem(QSpacerItem(*spacer_bottom))

        
    
        # Width of slices, crop, about
        bottom_l = QHBoxLayout()

        width_group = QGroupBox("Width of slices")
        width_group_layout = QHBoxLayout()
        self.width_slices_entry = QLineEdit("1080")
        self.width_slices_entry.setFixedWidth(slices_entry_width)
        width_slices_px = QLabel("px")
        width_slices_default = QLabel("Default: 1080px")
        width_slices_default.setDisabled(True)


        width_group_layout.addWidget(self.width_slices_entry)
        width_group_layout.addWidget(width_slices_px)
        width_group_layout.addSpacerItem(QSpacerItem(10, 0, QSizePolicy.Minimum))
        width_group_layout.addWidget(width_slices_default)
        width_group_layout.setSpacing(4)
        width_group_layout.addStretch(1)
        width_group.setLayout(width_group_layout)

        validator = QIntValidator(10, 10000, self)
        self.width_slices_entry.setValidator(validator)
        
        about_button = QPushButton("🔗 Hello!")
        about_button.setMinimumSize(*bottom_button_size)
        about_button.clicked.connect(lambda: webbrowser.open('https://under.martyr.shop/instagram-album-crop'))


        self.crop_button = QPushButton("🔪 Crop")
        self.crop_button.setMinimumSize(*bottom_button_size)
        self.crop_button.setEnabled(False)

        self.crop_button.clicked.connect(self.crop_handle)
        
        self._CropSignals = CropSignals()

        self._CropSignals.crop_started.connect(self.cropThreadStarted)
        self._CropSignals.crop_finished.connect(self.cropThreadFinished)
        self._CropSignals.crop_error.connect(self.cropThreadError)

        bottom_l.addWidget(width_group)
        bottom_l.addStretch(1)
        bottom_l.addWidget(about_button, alignment=Qt.AlignBottom)
        bottom_l.addWidget(self.crop_button, alignment=Qt.AlignBottom)

        grid.addLayout(bottom_l)
        

        self.setLayout(grid)


    @Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

    def entry_update(self, entry, directory):
        entry.setText(directory.replace('/', os.sep))

    def select_image(self):
        ftypes = "Image Files (*.jpg *.png)"
        image_dialog = QFileDialog.getOpenFileName(self, "Select the Instagram album image to be cropped", '', ftypes)
        # image_dialog is a tuple. First is file. Second is type of file.
        
        if not image_dialog[0]:
            return
        
        # fill variables declared in __init__
        self.image_to_crop = image_dialog[0]
        filename_and_ext = os.path.basename(self.image_to_crop)
        self.filename, self.extension = os.path.splitext(filename_and_ext)
        self.file_dir = os.path.dirname(os.path.realpath(self.image_to_crop))

        # update entry
        # self.entry_update(self.image_location, self.image_to_crop)
        self.entry_update(self.image_location, self.image_to_crop)

        # update save folder if a custom one has not been chosen
        if not self.save_folder_custom:
            self.save_folder_entry.setEnabled
            self.entry_update(self.save_folder_entry, self.file_dir)
            self.save_folder_entry.setDisabled

        self.crop_button.setEnabled(True)
        return

    def select_save_folder(self):
        save_folder_dialog = QFileDialog.getExistingDirectory(self, "Select the folder to save the images")
        if not save_folder_dialog:
            return
        self.save_folder_custom = save_folder_dialog
        self.entry_update(self.save_folder_entry, self.save_folder_custom)

    def crop_handle(self):
        threading.Thread(target=self.crop, daemon=True).start()

    def cropThreadStarted(self):
        self.crop_button.setEnabled(False)
        self.crop_button.setText("Cropping...")

    def cropThreadFinished(self):
        self.crop_button.setEnabled(True)
        self.crop_button.setText("🔪 Crop")

    def cropThreadError(self):
        QMessageBox.critical(self, "Error", "Can't open the file")
        self.crop_button.setEnabled(True)
        self.crop_button.setText("🔪 Crop")


    def crop(self):
        self._CropSignals.crop_started.emit()

        # load image
        try:
            im = Image.open(self.image_to_crop)
        except:
            self._CropSignals.crop_error.emit()
            return

        # calculate number of slices (float)
        width_im, height_im = im.size
        width_slices = int(self.width_slices_entry.text())
        number_slices = width_im/width_slices

        # add one more crop for images that are not multiple of the slice width
        # Will result in the last image being smaller in width of course
        if (number_slices % 1) != 0:
            number_slices += 1.0

        # set save_folder
    
        if self.save_folder_check.isChecked() or self.save_folder_custom == None:
            save_folder = self.file_dir
        else:
            save_folder = self.save_folder_custom.replace('/', os.sep)

        # common coordinates to each slice        
        top = 0
        bottom = height_im


        pool = mp.Pool()

        crops = [pool.apply_async(crop_process, (i, im, top, bottom, width_slices, width_im, save_folder, self.filename, self.extension,)) for i in range(int(number_slices))]

        for r in crops:
            r.wait()

        pool.close()
        pool.join()

        self._CropSignals.crop_finished.emit()

        # open folder after cropping
        if sys.platform == 'darwin':
            subprocess.call(['open', '--', save_folder])
        elif sys.platform == 'win32':
            subprocess.call(['explorer', save_folder])

if __name__ == "__main__": # to avoid new window with a new process in multiprocessing
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)

    mp.freeze_support() # support multiprocessing in pyinstaller

    widget = MainWidget()

    if sys.platform == 'darwin':
        widget.setFixedSize(600, 0)
    else:
        widget.setFixedSize(500, 0)

    widget.show()

    sys.exit(app.exec_())
