# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['instagram-crop.pyw'],
             pathex=['/Users/arecsu/instagram-album-crop'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

remove_binaries = [
				'qpdf', 'qtga', 'qgif', 'qsvg', 
				'd3dcompiler', 'libGLES', 'libEGL', 'opengl32sw', 
				'Qt5Pdf', 'Qt5Virtual', 'Qt5DBus', 'Qt5Quick', 
				'Qt5Svg', 'Qt5WebSockets', 'QtNetwork.pyd', 'qjpeg', 
				'qtiff', 'qwebp', 'qwebgl', 'QtQuick', 'QtPdf', 'QtSvg'
				]

remove_datas = ['qtbase']

def remove_from_list(input, keys):
    outlist = []
    for item in input:
        name, _, _ = item
        flag = 0
        for key_word in keys:
            if name.find(key_word) > -1:
                flag = 1
        if flag != 1:
            outlist.append(item)
    return outlist

a.binaries = remove_from_list(a.binaries, remove_binaries)
a.datas = remove_from_list(a.datas, remove_datas)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
			 name='Instagram Album Cropper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Instagram Album Cropper')
app = BUNDLE(coll,
             name='Instagram Album Cropper.app',
             icon=None,
             bundle_identifier=None)
