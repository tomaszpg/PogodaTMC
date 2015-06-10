/****************************************************************************
** Meta object code from reading C++ file 'minimap.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.0.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../pogoda/minimap.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'minimap.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.0.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
struct qt_meta_stringdata_MiniMap_t {
    QByteArrayData data[9];
    char stringdata[81];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    offsetof(qt_meta_stringdata_MiniMap_t, stringdata) + ofs \
        - idx * sizeof(QByteArrayData) \
    )
static const qt_meta_stringdata_MiniMap_t qt_meta_stringdata_MiniMap = {
    {
QT_MOC_LITERAL(0, 0, 7),
QT_MOC_LITERAL(1, 8, 7),
QT_MOC_LITERAL(2, 16, 0),
QT_MOC_LITERAL(3, 17, 7),
QT_MOC_LITERAL(4, 25, 10),
QT_MOC_LITERAL(5, 36, 10),
QT_MOC_LITERAL(6, 47, 12),
QT_MOC_LITERAL(7, 60, 12),
QT_MOC_LITERAL(8, 73, 6)
    },
    "MiniMap\0goToPos\0\0drawBox\0leftUpperX\0"
    "leftUpperY\0rightBottomX\0rightBottomY\0"
    "getBox\0"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_MiniMap[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
       3,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: name, argc, parameters, tag, flags
       1,    0,   29,    2, 0x08,
       3,    4,   30,    2, 0x08,
       8,    0,   39,    2, 0x0a,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int, QMetaType::Int, QMetaType::Int, QMetaType::Int,    4,    5,    6,    7,
    QMetaType::Void,

       0        // eod
};

void MiniMap::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        MiniMap *_t = static_cast<MiniMap *>(_o);
        switch (_id) {
        case 0: _t->goToPos(); break;
        case 1: _t->drawBox((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3])),(*reinterpret_cast< int(*)>(_a[4]))); break;
        case 2: _t->getBox(); break;
        default: ;
        }
    }
}

const QMetaObject MiniMap::staticMetaObject = {
    { &QDialog::staticMetaObject, qt_meta_stringdata_MiniMap.data,
      qt_meta_data_MiniMap,  qt_static_metacall, 0, 0}
};


const QMetaObject *MiniMap::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *MiniMap::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_MiniMap.stringdata))
        return static_cast<void*>(const_cast< MiniMap*>(this));
    return QDialog::qt_metacast(_clname);
}

int MiniMap::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QDialog::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 3)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 3;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 3)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 3;
    }
    return _id;
}
QT_END_MOC_NAMESPACE
