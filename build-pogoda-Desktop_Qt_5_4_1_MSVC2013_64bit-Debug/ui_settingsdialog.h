/********************************************************************************
** Form generated from reading UI file 'settingsdialog.ui'
**
** Created by: Qt User Interface Compiler version 5.4.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_SETTINGSDIALOG_H
#define UI_SETTINGSDIALOG_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDialog>
#include <QtWidgets/QDialogButtonBox>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QPushButton>

QT_BEGIN_NAMESPACE

class Ui_SettingsDialog
{
public:
    QDialogButtonBox *buttonBox;
    QComboBox *paramList;
    QGroupBox *groupBox;
    QLineEdit *nameEdit;
    QLineEdit *fileEdit;
    QLabel *label;
    QLabel *label_2;
    QPushButton *b_editRecord;
    QGroupBox *groupBox_2;
    QLineEdit *nameNew;
    QLineEdit *fileNew;
    QLabel *label_3;
    QLabel *label_4;
    QPushButton *b_addRecord;
    QPushButton *b_deleteRecord;
    QLineEdit *urlCore;
    QLabel *label_5;
    QLabel *label_6;
    QLineEdit *folderStr;
    QLabel *label_7;
    QLabel *label_8;
    QLineEdit *metaUrl;
    QLabel *urlLabel;
    QPushButton *b_saveToFile;
    QPushButton *b_loadFromFile;
    QPushButton *b_save_2;

    void setupUi(QDialog *SettingsDialog)
    {
        if (SettingsDialog->objectName().isEmpty())
            SettingsDialog->setObjectName(QStringLiteral("SettingsDialog"));
        SettingsDialog->resize(700, 320);
        buttonBox = new QDialogButtonBox(SettingsDialog);
        buttonBox->setObjectName(QStringLiteral("buttonBox"));
        buttonBox->setGeometry(QRect(580, 270, 91, 32));
        buttonBox->setOrientation(Qt::Horizontal);
        buttonBox->setStandardButtons(QDialogButtonBox::Ok);
        paramList = new QComboBox(SettingsDialog);
        paramList->setObjectName(QStringLiteral("paramList"));
        paramList->setGeometry(QRect(400, 20, 221, 22));
        groupBox = new QGroupBox(SettingsDialog);
        groupBox->setObjectName(QStringLiteral("groupBox"));
        groupBox->setGeometry(QRect(400, 50, 281, 80));
        nameEdit = new QLineEdit(groupBox);
        nameEdit->setObjectName(QStringLiteral("nameEdit"));
        nameEdit->setGeometry(QRect(80, 30, 141, 21));
        fileEdit = new QLineEdit(groupBox);
        fileEdit->setObjectName(QStringLiteral("fileEdit"));
        fileEdit->setGeometry(QRect(80, 50, 141, 21));
        label = new QLabel(groupBox);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(10, 30, 47, 13));
        label_2 = new QLabel(groupBox);
        label_2->setObjectName(QStringLiteral("label_2"));
        label_2->setGeometry(QRect(10, 50, 71, 16));
        b_editRecord = new QPushButton(groupBox);
        b_editRecord->setObjectName(QStringLiteral("b_editRecord"));
        b_editRecord->setGeometry(QRect(230, 30, 41, 41));
        groupBox_2 = new QGroupBox(SettingsDialog);
        groupBox_2->setObjectName(QStringLiteral("groupBox_2"));
        groupBox_2->setGeometry(QRect(400, 140, 281, 80));
        nameNew = new QLineEdit(groupBox_2);
        nameNew->setObjectName(QStringLiteral("nameNew"));
        nameNew->setGeometry(QRect(80, 30, 141, 21));
        fileNew = new QLineEdit(groupBox_2);
        fileNew->setObjectName(QStringLiteral("fileNew"));
        fileNew->setGeometry(QRect(80, 50, 141, 21));
        label_3 = new QLabel(groupBox_2);
        label_3->setObjectName(QStringLiteral("label_3"));
        label_3->setGeometry(QRect(10, 30, 47, 13));
        label_4 = new QLabel(groupBox_2);
        label_4->setObjectName(QStringLiteral("label_4"));
        label_4->setGeometry(QRect(10, 50, 71, 16));
        b_addRecord = new QPushButton(groupBox_2);
        b_addRecord->setObjectName(QStringLiteral("b_addRecord"));
        b_addRecord->setGeometry(QRect(230, 30, 41, 41));
        b_deleteRecord = new QPushButton(SettingsDialog);
        b_deleteRecord->setObjectName(QStringLiteral("b_deleteRecord"));
        b_deleteRecord->setGeometry(QRect(630, 20, 41, 21));
        urlCore = new QLineEdit(SettingsDialog);
        urlCore->setObjectName(QStringLiteral("urlCore"));
        urlCore->setGeometry(QRect(20, 50, 351, 21));
        label_5 = new QLabel(SettingsDialog);
        label_5->setObjectName(QStringLiteral("label_5"));
        label_5->setGeometry(QRect(20, 20, 341, 16));
        label_6 = new QLabel(SettingsDialog);
        label_6->setObjectName(QStringLiteral("label_6"));
        label_6->setGeometry(QRect(20, 80, 351, 16));
        folderStr = new QLineEdit(SettingsDialog);
        folderStr->setObjectName(QStringLiteral("folderStr"));
        folderStr->setGeometry(QRect(20, 110, 351, 21));
        label_7 = new QLabel(SettingsDialog);
        label_7->setObjectName(QStringLiteral("label_7"));
        label_7->setGeometry(QRect(20, 140, 371, 16));
        label_8 = new QLabel(SettingsDialog);
        label_8->setObjectName(QStringLiteral("label_8"));
        label_8->setGeometry(QRect(20, 180, 351, 16));
        metaUrl = new QLineEdit(SettingsDialog);
        metaUrl->setObjectName(QStringLiteral("metaUrl"));
        metaUrl->setGeometry(QRect(20, 210, 351, 21));
        urlLabel = new QLabel(SettingsDialog);
        urlLabel->setObjectName(QStringLiteral("urlLabel"));
        urlLabel->setGeometry(QRect(20, 240, 661, 16));
        b_saveToFile = new QPushButton(SettingsDialog);
        b_saveToFile->setObjectName(QStringLiteral("b_saveToFile"));
        b_saveToFile->setGeometry(QRect(200, 270, 91, 21));
        b_loadFromFile = new QPushButton(SettingsDialog);
        b_loadFromFile->setObjectName(QStringLiteral("b_loadFromFile"));
        b_loadFromFile->setGeometry(QRect(300, 270, 91, 21));
        b_save_2 = new QPushButton(SettingsDialog);
        b_save_2->setObjectName(QStringLiteral("b_save_2"));
        b_save_2->setGeometry(QRect(400, 270, 121, 21));

        retranslateUi(SettingsDialog);
        QObject::connect(buttonBox, SIGNAL(accepted()), SettingsDialog, SLOT(accept()));
        QObject::connect(buttonBox, SIGNAL(rejected()), SettingsDialog, SLOT(reject()));

        QMetaObject::connectSlotsByName(SettingsDialog);
    } // setupUi

    void retranslateUi(QDialog *SettingsDialog)
    {
        SettingsDialog->setWindowTitle(QApplication::translate("SettingsDialog", "Dialog", 0));
        groupBox->setTitle(QApplication::translate("SettingsDialog", "Edytuj rekord", 0));
        nameEdit->setText(QString());
        fileEdit->setText(QString());
        label->setText(QApplication::translate("SettingsDialog", "Opis", 0));
        label_2->setText(QApplication::translate("SettingsDialog", "Nazwa pliku", 0));
        b_editRecord->setText(QApplication::translate("SettingsDialog", "Zapisz", 0));
        groupBox_2->setTitle(QApplication::translate("SettingsDialog", "Nowy rekord", 0));
        label_3->setText(QApplication::translate("SettingsDialog", "Opis", 0));
        label_4->setText(QApplication::translate("SettingsDialog", "Nazwa pliku", 0));
        b_addRecord->setText(QApplication::translate("SettingsDialog", "Dodaj", 0));
        b_deleteRecord->setText(QApplication::translate("SettingsDialog", "Usu\305\204", 0));
        label_5->setText(QApplication::translate("SettingsDialog", "Rdze\305\204 URL: (np. http://ksgmet.eti.pg.gda.pl/prognozy/CSV/poland/  )", 0));
        label_6->setText(QApplication::translate("SettingsDialog", "Struktura folder\303\263w: (np. %y/%m/%d/%h/ )", 0));
        label_7->setText(QApplication::translate("SettingsDialog", "%y - rok,  %m - miesi\304\205c,  %d - dzie\305\204,  %h - godzina", 0));
        label_8->setText(QApplication::translate("SettingsDialog", "URL pliku opisowego (metadane):", 0));
        urlLabel->setText(QApplication::translate("SettingsDialog", "Przyk\305\202adowy URL:", 0));
        b_saveToFile->setText(QApplication::translate("SettingsDialog", "Zapisz do pliku", 0));
        b_loadFromFile->setText(QApplication::translate("SettingsDialog", "Wczytaj z pliku", 0));
        b_save_2->setText(QApplication::translate("SettingsDialog", "Resetuj ustawienia", 0));
    } // retranslateUi

};

namespace Ui {
    class SettingsDialog: public Ui_SettingsDialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_SETTINGSDIALOG_H
