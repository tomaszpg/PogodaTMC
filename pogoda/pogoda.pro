#-------------------------------------------------
#
# Project created by QtCreator 2015-04-10T12:47:55
#
#-------------------------------------------------

QT       += core gui\
            network


greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = pogoda
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    filedownloader.cpp \
    geolayer.cpp \
    viewport.cpp \
    clickablelabel.cpp \
    mapwindow.cpp \
    minimap.cpp \
    settingsdialog.cpp

HEADERS  += mainwindow.h \
    filedownloader.h \
    geolayer.h \
    viewport.h \
    clickablelabel.h \
    mapwindow.h \
    minimap.h \
    settingsdialog.h

FORMS    += mainwindow.ui \
    mapwindow.ui \
    minimap.ui \
    settingsdialog.ui

unix|win32: LIBS += -L$$PWD/FWTools2.4.7/lib/ -lgdal_i

INCLUDEPATH += $$_PRO_FILE_PWD_/FWTools2.4.7/include
DEPENDPATH += $$_PRO_FILE_PWD_/FWTools2.4.7/include

unix|win32: LIBS += -L$$_PRO_FILE_PWD_/FWTools2.4.7/lib/ -lgdal_i

INCLUDEPATH += $$_PRO_FILE_PWD_/FWTools2.4.7/include
DEPENDPATH += $$_PRO_FILE_PWD_/FWTools2.4.7/include

win32:CONFIG(release, debug|release): LIBS += -L$$PWD/../../takie_tam/studia/mapy_cyfrowe/laboratorium/TMCLab1/FWTools2.4.7/lib/ -lgdal_i
else:win32:CONFIG(debug, debug|release): LIBS += -L$$PWD/../../takie_tam/studia/mapy_cyfrowe/laboratorium/TMCLab1/FWTools2.4.7/lib/ -lgdal_i
else:unix: LIBS += -L$$PWD/../../takie_tam/studia/mapy_cyfrowe/laboratorium/TMCLab1/FWTools2.4.7/lib/ -lgdal_i

INCLUDEPATH += $$PWD/../../takie_tam/studia/mapy_cyfrowe/laboratorium/TMCLab1/FWTools2.4.7/include
DEPENDPATH += $$PWD/../../takie_tam/studia/mapy_cyfrowe/laboratorium/TMCLab1/FWTools2.4.7/include
