from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': ["tkinter"]}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None


executables = [
    Executable('instagram_crop.py', base=base)
]

setup(name='Instagram Album Cropper',
      version = '1.01',
      description = 'Instagram Album Cropper',
      options = {'build_exe': build_options},
      executables = executables)
