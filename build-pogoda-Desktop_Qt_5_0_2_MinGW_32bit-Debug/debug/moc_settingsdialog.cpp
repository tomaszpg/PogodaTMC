/****************************************************************************
** Meta object code from reading C++ file 'settingsdialog.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.0.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../pogoda/settingsdialog.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'settingsdialog.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.0.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
struct qt_meta_stringdata_SettingsDialog_t {
    QByteArrayData data[23];
    char stringdata[359];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    offsetof(qt_meta_stringdata_SettingsDialog_t, stringdata) + ofs \
        - idx * sizeof(QByteArrayData) \
    )
static const qt_meta_stringdata_SettingsDialog_t qt_meta_stringdata_SettingsDialog = {
    {
QT_MOC_LITERAL(0, 0, 14),
QT_MOC_LITERAL(1, 15, 15),
QT_MOC_LITERAL(2, 31, 0),
QT_MOC_LITERAL(3, 32, 16),
QT_MOC_LITERAL(4, 49, 13),
QT_MOC_LITERAL(5, 63, 32),
QT_MOC_LITERAL(6, 96, 4),
QT_MOC_LITERAL(7, 101, 23),
QT_MOC_LITERAL(8, 125, 22),
QT_MOC_LITERAL(9, 148, 25),
QT_MOC_LITERAL(10, 174, 19),
QT_MOC_LITERAL(11, 194, 24),
QT_MOC_LITERAL(12, 219, 22),
QT_MOC_LITERAL(13, 242, 22),
QT_MOC_LITERAL(14, 265, 21),
QT_MOC_LITERAL(15, 287, 10),
QT_MOC_LITERAL(16, 298, 14),
QT_MOC_LITERAL(17, 313, 12),
QT_MOC_LITERAL(18, 326, 8),
QT_MOC_LITERAL(19, 335, 4),
QT_MOC_LITERAL(20, 340, 4),
QT_MOC_LITERAL(21, 345, 5),
QT_MOC_LITERAL(22, 351, 6)
    },
    "SettingsDialog\0settingsChanged\0\0"
    "setDefaultValues\0updateExample\0"
    "on_paramList_currentIndexChanged\0arg1\0"
    "on_b_editRecord_clicked\0on_b_addRecord_clicked\0"
    "on_b_deleteRecord_clicked\0on_b_save_2_clicked\0"
    "on_folderStr_textChanged\0"
    "on_urlCore_textChanged\0on_metaUrl_textChanged\0"
    "on_buttonBox_accepted\0getMetaUrl\0"
    "getParamNumber\0getParamList\0QString*\0"
    "str1\0str2\0index\0getUrl\0"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_SettingsDialog[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
      16,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,   94,    2, 0x05,

 // slots: name, argc, parameters, tag, flags
       3,    0,   95,    2, 0x08,
       4,    0,   96,    2, 0x08,
       5,    1,   97,    2, 0x08,
       7,    0,  100,    2, 0x08,
       8,    0,  101,    2, 0x08,
       9,    0,  102,    2, 0x08,
      10,    0,  103,    2, 0x08,
      11,    1,  104,    2, 0x08,
      12,    1,  107,    2, 0x08,
      13,    1,  110,    2, 0x08,
      14,    0,  113,    2, 0x08,
      15,    0,  114,    2, 0x0a,
      16,    0,  115,    2, 0x0a,
      17,    3,  116,    2, 0x0a,
      22,    0,  123,    2, 0x0a,

 // signals: parameters
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::QString,    6,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::QString,    6,
    QMetaType::Void, QMetaType::QString,    6,
    QMetaType::Void, QMetaType::QString,    6,
    QMetaType::Void,
    QMetaType::QString,
    QMetaType::Int,
    QMetaType::Void, 0x80000000 | 18, 0x80000000 | 18, QMetaType::Int,   19,   20,   21,
    QMetaType::QString,

       0        // eod
};

void SettingsDialog::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        SettingsDialog *_t = static_cast<SettingsDialog *>(_o);
        switch (_id) {
        case 0: _t->settingsChanged(); break;
        case 1: _t->setDefaultValues(); break;
        case 2: _t->updateExample(); break;
        case 3: _t->on_paramList_currentIndexChanged((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 4: _t->on_b_editRecord_clicked(); break;
        case 5: _t->on_b_addRecord_clicked(); break;
        case 6: _t->on_b_deleteRecord_clicked(); break;
        case 7: _t->on_b_save_2_clicked(); break;
        case 8: _t->on_folderStr_textChanged((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 9: _t->on_urlCore_textChanged((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 10: _t->on_metaUrl_textChanged((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 11: _t->on_buttonBox_accepted(); break;
        case 12: { QString _r = _t->getMetaUrl();
            if (_a[0]) *reinterpret_cast< QString*>(_a[0]) = _r; }  break;
        case 13: { int _r = _t->getParamNumber();
            if (_a[0]) *reinterpret_cast< int*>(_a[0]) = _r; }  break;
        case 14: _t->getParamList((*reinterpret_cast< QString*(*)>(_a[1])),(*reinterpret_cast< QString*(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3]))); break;
        case 15: { QString _r = _t->getUrl();
            if (_a[0]) *reinterpret_cast< QString*>(_a[0]) = _r; }  break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        void **func = reinterpret_cast<void **>(_a[1]);
        {
            typedef void (SettingsDialog::*_t)();
            if (*reinterpret_cast<_t *>(func) == static_cast<_t>(&SettingsDialog::settingsChanged)) {
                *result = 0;
            }
        }
    }
}

const QMetaObject SettingsDialog::staticMetaObject = {
    { &QDialog::staticMetaObject, qt_meta_stringdata_SettingsDialog.data,
      qt_meta_data_SettingsDialog,  qt_static_metacall, 0, 0}
};


const QMetaObject *SettingsDialog::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *SettingsDialog::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_SettingsDialog.stringdata))
        return static_cast<void*>(const_cast< SettingsDialog*>(this));
    return QDialog::qt_metacast(_clname);
}

int SettingsDialog::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QDialog::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 16)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 16;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 16)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 16;
    }
    return _id;
}

// SIGNAL 0
void SettingsDialog::settingsChanged()
{
    QMetaObject::activate(this, &staticMetaObject, 0, 0);
}
QT_END_MOC_NAMESPACE
