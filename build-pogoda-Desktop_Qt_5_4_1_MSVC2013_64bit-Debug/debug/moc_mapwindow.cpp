/****************************************************************************
** Meta object code from reading C++ file 'mapwindow.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.4.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../pogoda/mapwindow.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'mapwindow.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.4.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
struct qt_meta_stringdata_MapWindow_t {
    QByteArrayData data[14];
    char stringdata[125];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_MapWindow_t, stringdata) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_MapWindow_t qt_meta_stringdata_MapWindow = {
    {
QT_MOC_LITERAL(0, 0, 9), // "MapWindow"
QT_MOC_LITERAL(1, 10, 12), // "resizeSignal"
QT_MOC_LITERAL(2, 23, 0), // ""
QT_MOC_LITERAL(3, 24, 9), // "getHandle"
QT_MOC_LITERAL(4, 34, 9), // "Viewport*"
QT_MOC_LITERAL(5, 44, 9), // "drawImage"
QT_MOC_LITERAL(6, 54, 5), // "image"
QT_MOC_LITERAL(7, 60, 8), // "getLabel"
QT_MOC_LITERAL(8, 69, 15), // "clickableLabel*"
QT_MOC_LITERAL(9, 85, 11), // "resizeEvent"
QT_MOC_LITERAL(10, 97, 13), // "QResizeEvent*"
QT_MOC_LITERAL(11, 111, 9), // "resizeMap"
QT_MOC_LITERAL(12, 121, 1), // "w"
QT_MOC_LITERAL(13, 123, 1) // "h"

    },
    "MapWindow\0resizeSignal\0\0getHandle\0"
    "Viewport*\0drawImage\0image\0getLabel\0"
    "clickableLabel*\0resizeEvent\0QResizeEvent*\0"
    "resizeMap\0w\0h"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_MapWindow[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
       6,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,   44,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       3,    0,   45,    2, 0x0a /* Public */,
       5,    1,   46,    2, 0x0a /* Public */,
       7,    0,   49,    2, 0x0a /* Public */,
       9,    1,   50,    2, 0x08 /* Private */,
      11,    2,   53,    2, 0x08 /* Private */,

 // signals: parameters
    QMetaType::Void,

 // slots: parameters
    0x80000000 | 4,
    QMetaType::Void, QMetaType::QImage,    6,
    0x80000000 | 8,
    QMetaType::Void, 0x80000000 | 10,    2,
    QMetaType::Void, QMetaType::Int, QMetaType::Int,   12,   13,

       0        // eod
};

void MapWindow::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        MapWindow *_t = static_cast<MapWindow *>(_o);
        switch (_id) {
        case 0: _t->resizeSignal(); break;
        case 1: { Viewport* _r = _t->getHandle();
            if (_a[0]) *reinterpret_cast< Viewport**>(_a[0]) = _r; }  break;
        case 2: _t->drawImage((*reinterpret_cast< QImage(*)>(_a[1]))); break;
        case 3: { clickableLabel* _r = _t->getLabel();
            if (_a[0]) *reinterpret_cast< clickableLabel**>(_a[0]) = _r; }  break;
        case 4: _t->resizeEvent((*reinterpret_cast< QResizeEvent*(*)>(_a[1]))); break;
        case 5: _t->resizeMap((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        void **func = reinterpret_cast<void **>(_a[1]);
        {
            typedef void (MapWindow::*_t)();
            if (*reinterpret_cast<_t *>(func) == static_cast<_t>(&MapWindow::resizeSignal)) {
                *result = 0;
            }
        }
    }
}

const QMetaObject MapWindow::staticMetaObject = {
    { &QDialog::staticMetaObject, qt_meta_stringdata_MapWindow.data,
      qt_meta_data_MapWindow,  qt_static_metacall, Q_NULLPTR, Q_NULLPTR}
};


const QMetaObject *MapWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *MapWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return Q_NULLPTR;
    if (!strcmp(_clname, qt_meta_stringdata_MapWindow.stringdata))
        return static_cast<void*>(const_cast< MapWindow*>(this));
    return QDialog::qt_metacast(_clname);
}

int MapWindow::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QDialog::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 6)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 6;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 6)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 6;
    }
    return _id;
}

// SIGNAL 0
void MapWindow::resizeSignal()
{
    QMetaObject::activate(this, &staticMetaObject, 0, Q_NULLPTR);
}
QT_END_MOC_NAMESPACE
