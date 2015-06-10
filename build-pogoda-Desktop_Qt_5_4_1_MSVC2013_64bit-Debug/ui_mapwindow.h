/********************************************************************************
** Form generated from reading UI file 'mapwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.4.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAPWINDOW_H
#define UI_MAPWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDialog>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QWidget>
#include <clickablelabel.h>

QT_BEGIN_NAMESPACE

class Ui_MapWindow
{
public:
    clickableLabel *label;
    QWidget *legendGroup;
    QLabel *labelMax;
    QLabel *labelParam;
    QLabel *gradientLabel;
    QLabel *labelMin;

    void setupUi(QDialog *MapWindow)
    {
        if (MapWindow->objectName().isEmpty())
            MapWindow->setObjectName(QStringLiteral("MapWindow"));
        MapWindow->resize(552, 552);
        QSizePolicy sizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(MapWindow->sizePolicy().hasHeightForWidth());
        MapWindow->setSizePolicy(sizePolicy);
        MapWindow->setMinimumSize(QSize(552, 552));
        label = new clickableLabel(MapWindow);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(40, 0, 512, 512));
        QSizePolicy sizePolicy1(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(label->sizePolicy().hasHeightForWidth());
        label->setSizePolicy(sizePolicy1);
        label->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        legendGroup = new QWidget(MapWindow);
        legendGroup->setObjectName(QStringLiteral("legendGroup"));
        legendGroup->setGeometry(QRect(90, 520, 450, 25));
        labelMax = new QLabel(legendGroup);
        labelMax->setObjectName(QStringLiteral("labelMax"));
        labelMax->setGeometry(QRect(390, 0, 47, 16));
        labelMax->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        labelParam = new QLabel(legendGroup);
        labelParam->setObjectName(QStringLiteral("labelParam"));
        labelParam->setGeometry(QRect(10, 0, 151, 16));
        labelParam->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        gradientLabel = new QLabel(legendGroup);
        gradientLabel->setObjectName(QStringLiteral("gradientLabel"));
        gradientLabel->setGeometry(QRect(230, 0, 150, 20));
        gradientLabel->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);
        labelMin = new QLabel(legendGroup);
        labelMin->setObjectName(QStringLiteral("labelMin"));
        labelMin->setGeometry(QRect(170, 0, 51, 16));
        labelMin->setAlignment(Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter);

        retranslateUi(MapWindow);

        QMetaObject::connectSlotsByName(MapWindow);
    } // setupUi

    void retranslateUi(QDialog *MapWindow)
    {
        MapWindow->setWindowTitle(QApplication::translate("MapWindow", "Mapa", 0));
        label->setText(QString());
        labelMax->setText(QString());
        labelParam->setText(QString());
        gradientLabel->setText(QString());
        labelMin->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class MapWindow: public Ui_MapWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAPWINDOW_H
