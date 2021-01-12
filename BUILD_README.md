In all cases, a clean virtalenv environment is recommended.

Use Python 3.8.x

$ pip install --upgrade pip
$ pip install -r requeriments.txt

# Mac Specific
Use cx_freeze

$ pip install cx_freeze
$ ./build_macos.sh

# Windows Specific

$ pip install pyinstaller
$ pyinstaller --clean build_windows.spec
