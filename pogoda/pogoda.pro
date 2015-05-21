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
    mapwindow.cpp

HEADERS  += mainwindow.h \
    filedownloader.h \
    geolayer.h \
    viewport.h \
    clickablelabel.h \
    mapwindow.h

FORMS    += mainwindow.ui \
    mapwindow.ui
