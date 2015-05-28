/****************************************************************************
** Meta object code from reading C++ file 'mapwindow.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.0.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../mapwindow.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'mapwindow.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.0.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
struct qt_meta_stringdata_MapWindow_t {
    QByteArrayData data[20];
    char stringdata[172];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    offsetof(qt_meta_stringdata_MapWindow_t, stringdata) + ofs \
        - idx * sizeof(QByteArrayData) \
    )
static const qt_meta_stringdata_MapWindow_t qt_meta_stringdata_MapWindow = {
    {
QT_MOC_LITERAL(0, 0, 9),
QT_MOC_LITERAL(1, 10, 12),
QT_MOC_LITERAL(2, 23, 0),
QT_MOC_LITERAL(3, 24, 9),
QT_MOC_LITERAL(4, 34, 9),
QT_MOC_LITERAL(5, 44, 9),
QT_MOC_LITERAL(6, 54, 5),
QT_MOC_LITERAL(7, 60, 8),
QT_MOC_LITERAL(8, 69, 15),
QT_MOC_LITERAL(9, 85, 14),
QT_MOC_LITERAL(10, 100, 3),
QT_MOC_LITERAL(11, 104, 3),
QT_MOC_LITERAL(12, 108, 4),
QT_MOC_LITERAL(13, 113, 8),
QT_MOC_LITERAL(14, 122, 8),
QT_MOC_LITERAL(15, 131, 11),
QT_MOC_LITERAL(16, 143, 13),
QT_MOC_LITERAL(17, 157, 9),
QT_MOC_LITERAL(18, 167, 1),
QT_MOC_LITERAL(19, 169, 1)
    },
    "MapWindow\0resizeSignal\0\0getHandle\0"
    "Viewport*\0drawImage\0image\0getLabel\0"
    "clickableLabel*\0updateGradient\0min\0"
    "max\0text\0colorMin\0colorMax\0resizeEvent\0"
    "QResizeEvent*\0resizeMap\0w\0h\0"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_MapWindow[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
       7,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,   49,    2, 0x05,

 // slots: name, argc, parameters, tag, flags
       3,    0,   50,    2, 0x0a,
       5,    1,   51,    2, 0x0a,
       7,    0,   54,    2, 0x0a,
       9,    5,   55,    2, 0x0a,
      15,    1,   66,    2, 0x08,
      17,    2,   69,    2, 0x08,

 // signals: parameters
    QMetaType::Void,

 // slots: parameters
    0x80000000 | 4,
    QMetaType::Void, QMetaType::QImage,    6,
    0x80000000 | 8,
    QMetaType::Void, QMetaType::Float, QMetaType::Float, QMetaType::QString, QMetaType::QColor, QMetaType::QColor,   10,   11,   12,   13,   14,
    QMetaType::Void, 0x80000000 | 16,    2,
    QMetaType::Void, QMetaType::Int, QMetaType::Int,   18,   19,

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
        case 4: _t->updateGradient((*reinterpret_cast< float(*)>(_a[1])),(*reinterpret_cast< float(*)>(_a[2])),(*reinterpret_cast< QString(*)>(_a[3])),(*reinterpret_cast< QColor(*)>(_a[4])),(*reinterpret_cast< QColor(*)>(_a[5]))); break;
        case 5: _t->resizeEvent((*reinterpret_cast< QResizeEvent*(*)>(_a[1]))); break;
        case 6: _t->resizeMap((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
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
      qt_meta_data_MapWindow,  qt_static_metacall, 0, 0}
};


const QMetaObject *MapWindow::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *MapWindow::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
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
        if (_id < 7)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 7;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 7)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 7;
    }
    return _id;
}

// SIGNAL 0
void MapWindow::resizeSignal()
{
    QMetaObject::activate(this, &staticMetaObject, 0, 0);
}
QT_END_MOC_NAMESPACE
