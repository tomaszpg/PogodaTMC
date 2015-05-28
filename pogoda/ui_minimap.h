/********************************************************************************
** Form generated from reading UI file 'minimap.ui'
**
** Created by: Qt User Interface Compiler version 5.0.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MINIMAP_H
#define UI_MINIMAP_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDialog>
#include <QtWidgets/QHeaderView>
#include <clickablelabel.h>

QT_BEGIN_NAMESPACE

class Ui_MiniMap
{
public:
    clickableLabel *labelMap;

    void setupUi(QDialog *MiniMap)
    {
        if (MiniMap->objectName().isEmpty())
            MiniMap->setObjectName(QStringLiteral("MiniMap"));
        MiniMap->resize(256, 256);
        QSizePolicy sizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(MiniMap->sizePolicy().hasHeightForWidth());
        MiniMap->setSizePolicy(sizePolicy);
        MiniMap->setMinimumSize(QSize(256, 256));
        MiniMap->setMaximumSize(QSize(256, 256));
        labelMap = new clickableLabel(MiniMap);
        labelMap->setObjectName(QStringLiteral("labelMap"));
        labelMap->setGeometry(QRect(0, 0, 256, 256));

        retranslateUi(MiniMap);

        QMetaObject::connectSlotsByName(MiniMap);
    } // setupUi

    void retranslateUi(QDialog *MiniMap)
    {
        MiniMap->setWindowTitle(QApplication::translate("MiniMap", "Minimapa", 0));
        labelMap->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class MiniMap: public Ui_MiniMap {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MINIMAP_H
