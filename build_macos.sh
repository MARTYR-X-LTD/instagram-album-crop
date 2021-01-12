rm -rf build

python build_macos.py bdist_mac --iconfile=icons/icon.icns

rm -rf build/exe.macos*

BUILD_DIR=build/Instag*/Contents/MacOS

# make it lightweight deleting unused things
# rm -f $BUILD_DIR/*.dylib
# rm -f $BUILD_DIR/Qt*

rm -rf $BUILD_DIR/lib/asyncio
rm -rf $BUILD_DIR/lib/concurrent
rm -rf $BUILD_DIR/lib/ctypes
rm -rf $BUILD_DIR/lib/distutils
rm -rf $BUILD_DIR/lib/emails
rm -rf $BUILD_DIR/lib/html
rm -rf $BUILD_DIR/lib/http
rm -rf $BUILD_DIR/lib/emails
rm -rf $BUILD_DIR/lib/lib2to3
rm -rf $BUILD_DIR/lib/pydoc_data
rm -rf $BUILD_DIR/lib/test
rm -rf $BUILD_DIR/lib/unittest
rm -rf $BUILD_DIR/lib/xmlrpc
rm -rf $BUILD_DIR/lib/PyQt5/*.pyi
rm -rf $BUILD_DIR/lib/PyQt5/QtQuick.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtQml.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtXml.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtMultimedia.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtQuick.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtNetwork.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtLocation.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtBluetooth.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtDesigner.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtSql.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtSensors.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtPrintSupport.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtHelp.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtDBus.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtPositioning.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtNetworkAuth.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtNfc.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtSvg.abi*
rm -rf $BUILD_DIR/lib/PyQt5/QtTest.abi*

rm -rf $BUILD_DIR/lib/PyQt5/bindings
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtBluetooth*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtConcurrent*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtHelp*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtLocation*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtMultimedia*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtNetwork*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtNfc*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtPositioning*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtQml*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtQuick*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtRemote*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtSensors*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtSerial*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtSql*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtSvg*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtTest*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtWeb*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtXml*
rm -rf $BUILD_DIR/lib/PyQt5/Qt/lib/QtDesigner*


mv $BUILD_DIR/lib/PyQt5/Qt/plugins/platforms $BUILD_DIR/lib/PyQt5/Qt/
mv $BUILD_DIR/lib/PyQt5/Qt/plugins/styles $BUILD_DIR/lib/PyQt5/Qt/
rm -rf $BUILD_DIR/lib/PyQt5/Qt/plugins/*
mv $BUILD_DIR/lib/PyQt5/Qt/platforms $BUILD_DIR/lib/PyQt5/Qt/plugins/
mv $BUILD_DIR/lib/PyQt5/Qt/styles $BUILD_DIR/lib/PyQt5/Qt/plugins/


rm -rf $BUILD_DIR/lib/PyQt5/Qt/qml
rm -rf $BUILD_DIR/lib/PyQt5/Qt/qsci
rm -rf $BUILD_DIR/lib/PyQt5/Qt/translations
rm -rf $BUILD_DIR/lib/PyQt5/uic
