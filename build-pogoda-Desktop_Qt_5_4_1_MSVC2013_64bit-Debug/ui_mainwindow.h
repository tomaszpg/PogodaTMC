/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.4.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QCalendarWidget>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QGraphicsView>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QTreeWidget>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *actionUstawienia_programu;
    QAction *actionO_programie;
    QAction *actionWyj_cie;
    QWidget *centralWidget;
    QTabWidget *tabMapType;
    QWidget *tab_gdal;
    QPushButton *bLayerUp;
    QPushButton *bLayerDown;
    QPushButton *bLayerNew;
    QPushButton *bLayerVisibility;
    QPushButton *bLayerDelete;
    QTreeWidget *treeWidget;
    QWidget *tab_osm;
    QTextEdit *textEdit;
    QTextEdit *textEdit_2;
    QPushButton *pushButton;
    QLabel *label_5;
    QLabel *label_6;
    QLabel *label_MapType;
    QPushButton *bNavUp;
    QPushButton *bNavDown;
    QPushButton *bNavRight;
    QPushButton *bNavLeft;
    QLabel *label_textScale;
    QLabel *labelScale;
    QPushButton *bNavUp_2;
    QPushButton *bNavUp_3;
    QGroupBox *groupWeather;
    QComboBox *comboHour;
    QLabel *label_hour;
    QCalendarWidget *calendarWidget;
    QLabel *label_date;
    QCheckBox *checkBox;
    QGroupBox *groupAdvanced;
    QLabel *label_param;
    QComboBox *comboParam;
    QCheckBox *checkFilter;
    QLabel *label_color;
    QPushButton *bColor1;
    QPushButton *bColor2;
    QGroupBox *groupFilter;
    QLabel *label;
    QLabel *label_2;
    QLineEdit *lineHigher;
    QLineEdit *lineLower;
    QPushButton *bShowWeather;
    QGroupBox *groupGraph;
    QLabel *label_graph;
    QComboBox *comboGraph;
    QGraphicsView *graphicsGraph;
    QLabel *labelLog;
    QLabel *label_3;
    QLabel *label_4;
    QMenuBar *menuBar;
    QMenu *menuPogoda;
    QMenu *menuPomoc;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(430, 620);
        QSizePolicy sizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(MainWindow->sizePolicy().hasHeightForWidth());
        MainWindow->setSizePolicy(sizePolicy);
        MainWindow->setMinimumSize(QSize(430, 620));
        MainWindow->setMaximumSize(QSize(500, 620));
        MainWindow->setMouseTracking(false);
        actionUstawienia_programu = new QAction(MainWindow);
        actionUstawienia_programu->setObjectName(QStringLiteral("actionUstawienia_programu"));
        actionO_programie = new QAction(MainWindow);
        actionO_programie->setObjectName(QStringLiteral("actionO_programie"));
        actionWyj_cie = new QAction(MainWindow);
        actionWyj_cie->setObjectName(QStringLiteral("actionWyj_cie"));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        tabMapType = new QTabWidget(centralWidget);
        tabMapType->setObjectName(QStringLiteral("tabMapType"));
        tabMapType->setGeometry(QRect(10, 30, 411, 141));
        tab_gdal = new QWidget();
        tab_gdal->setObjectName(QStringLiteral("tab_gdal"));
        bLayerUp = new QPushButton(tab_gdal);
        bLayerUp->setObjectName(QStringLiteral("bLayerUp"));
        bLayerUp->setGeometry(QRect(220, 10, 71, 23));
        bLayerDown = new QPushButton(tab_gdal);
        bLayerDown->setObjectName(QStringLiteral("bLayerDown"));
        bLayerDown->setGeometry(QRect(220, 40, 71, 23));
        bLayerNew = new QPushButton(tab_gdal);
        bLayerNew->setObjectName(QStringLiteral("bLayerNew"));
        bLayerNew->setGeometry(QRect(300, 10, 91, 23));
        bLayerVisibility = new QPushButton(tab_gdal);
        bLayerVisibility->setObjectName(QStringLiteral("bLayerVisibility"));
        bLayerVisibility->setGeometry(QRect(220, 70, 71, 23));
        bLayerDelete = new QPushButton(tab_gdal);
        bLayerDelete->setObjectName(QStringLiteral("bLayerDelete"));
        bLayerDelete->setGeometry(QRect(300, 40, 91, 23));
        treeWidget = new QTreeWidget(tab_gdal);
        treeWidget->setObjectName(QStringLiteral("treeWidget"));
        treeWidget->setGeometry(QRect(10, 10, 201, 91));
        treeWidget->setRootIsDecorated(true);
        tabMapType->addTab(tab_gdal, QString());
        tab_osm = new QWidget();
        tab_osm->setObjectName(QStringLiteral("tab_osm"));
        textEdit = new QTextEdit(tab_osm);
        textEdit->setObjectName(QStringLiteral("textEdit"));
        textEdit->setGeometry(QRect(50, 10, 104, 21));
        textEdit_2 = new QTextEdit(tab_osm);
        textEdit_2->setObjectName(QStringLiteral("textEdit_2"));
        textEdit_2->setGeometry(QRect(50, 40, 104, 21));
        pushButton = new QPushButton(tab_osm);
        pushButton->setObjectName(QStringLiteral("pushButton"));
        pushButton->setGeometry(QRect(240, 60, 75, 23));
        label_5 = new QLabel(tab_osm);
        label_5->setObjectName(QStringLiteral("label_5"));
        label_5->setGeometry(QRect(10, 10, 41, 20));
        label_6 = new QLabel(tab_osm);
        label_6->setObjectName(QStringLiteral("label_6"));
        label_6->setGeometry(QRect(10, 40, 31, 20));
        tabMapType->addTab(tab_osm, QString());
        label_MapType = new QLabel(centralWidget);
        label_MapType->setObjectName(QStringLiteral("label_MapType"));
        label_MapType->setGeometry(QRect(20, 10, 111, 16));
        bNavUp = new QPushButton(centralWidget);
        bNavUp->setObjectName(QStringLiteral("bNavUp"));
        bNavUp->setGeometry(QRect(360, 430, 31, 31));
        bNavDown = new QPushButton(centralWidget);
        bNavDown->setObjectName(QStringLiteral("bNavDown"));
        bNavDown->setGeometry(QRect(360, 490, 31, 31));
        bNavRight = new QPushButton(centralWidget);
        bNavRight->setObjectName(QStringLiteral("bNavRight"));
        bNavRight->setGeometry(QRect(390, 460, 31, 31));
        bNavLeft = new QPushButton(centralWidget);
        bNavLeft->setObjectName(QStringLiteral("bNavLeft"));
        bNavLeft->setGeometry(QRect(330, 460, 31, 31));
        label_textScale = new QLabel(centralWidget);
        label_textScale->setObjectName(QStringLiteral("label_textScale"));
        label_textScale->setGeometry(QRect(330, 390, 31, 16));
        labelScale = new QLabel(centralWidget);
        labelScale->setObjectName(QStringLiteral("labelScale"));
        labelScale->setGeometry(QRect(330, 410, 91, 16));
        bNavUp_2 = new QPushButton(centralWidget);
        bNavUp_2->setObjectName(QStringLiteral("bNavUp_2"));
        bNavUp_2->setGeometry(QRect(360, 390, 21, 21));
        bNavUp_3 = new QPushButton(centralWidget);
        bNavUp_3->setObjectName(QStringLiteral("bNavUp_3"));
        bNavUp_3->setGeometry(QRect(380, 390, 21, 21));
        groupWeather = new QGroupBox(centralWidget);
        groupWeather->setObjectName(QStringLiteral("groupWeather"));
        groupWeather->setEnabled(true);
        groupWeather->setGeometry(QRect(10, 180, 411, 201));
        comboHour = new QComboBox(groupWeather);
        comboHour->setObjectName(QStringLiteral("comboHour"));
        comboHour->setGeometry(QRect(230, 40, 51, 22));
        label_hour = new QLabel(groupWeather);
        label_hour->setObjectName(QStringLiteral("label_hour"));
        label_hour->setGeometry(QRect(230, 20, 51, 16));
        calendarWidget = new QCalendarWidget(groupWeather);
        calendarWidget->setObjectName(QStringLiteral("calendarWidget"));
        calendarWidget->setGeometry(QRect(10, 40, 216, 155));
        label_date = new QLabel(groupWeather);
        label_date->setObjectName(QStringLiteral("label_date"));
        label_date->setGeometry(QRect(10, 20, 51, 16));
        checkBox = new QCheckBox(groupWeather);
        checkBox->setObjectName(QStringLiteral("checkBox"));
        checkBox->setGeometry(QRect(290, 40, 121, 17));
        checkBox->setChecked(true);
        groupAdvanced = new QGroupBox(groupWeather);
        groupAdvanced->setObjectName(QStringLiteral("groupAdvanced"));
        groupAdvanced->setEnabled(true);
        groupAdvanced->setGeometry(QRect(230, 70, 181, 131));
        label_param = new QLabel(groupAdvanced);
        label_param->setObjectName(QStringLiteral("label_param"));
        label_param->setGeometry(QRect(10, 0, 51, 16));
        comboParam = new QComboBox(groupAdvanced);
        comboParam->setObjectName(QStringLiteral("comboParam"));
        comboParam->setGeometry(QRect(10, 20, 161, 22));
        checkFilter = new QCheckBox(groupAdvanced);
        checkFilter->setObjectName(QStringLiteral("checkFilter"));
        checkFilter->setGeometry(QRect(120, 60, 51, 17));
        label_color = new QLabel(groupAdvanced);
        label_color->setObjectName(QStringLiteral("label_color"));
        label_color->setGeometry(QRect(10, 50, 41, 16));
        bColor1 = new QPushButton(groupAdvanced);
        bColor1->setObjectName(QStringLiteral("bColor1"));
        bColor1->setGeometry(QRect(50, 50, 21, 21));
        bColor2 = new QPushButton(groupAdvanced);
        bColor2->setObjectName(QStringLiteral("bColor2"));
        bColor2->setGeometry(QRect(70, 50, 21, 21));
        groupFilter = new QGroupBox(groupAdvanced);
        groupFilter->setObjectName(QStringLiteral("groupFilter"));
        groupFilter->setEnabled(false);
        groupFilter->setGeometry(QRect(10, 80, 161, 41));
        label = new QLabel(groupFilter);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(10, 10, 16, 16));
        label_2 = new QLabel(groupFilter);
        label_2->setObjectName(QStringLiteral("label_2"));
        label_2->setGeometry(QRect(90, 10, 16, 16));
        lineHigher = new QLineEdit(groupFilter);
        lineHigher->setObjectName(QStringLiteral("lineHigher"));
        lineHigher->setGeometry(QRect(20, 10, 51, 20));
        lineLower = new QLineEdit(groupFilter);
        lineLower->setObjectName(QStringLiteral("lineLower"));
        lineLower->setGeometry(QRect(100, 10, 51, 20));
        bShowWeather = new QPushButton(groupWeather);
        bShowWeather->setObjectName(QStringLiteral("bShowWeather"));
        bShowWeather->setGeometry(QRect(330, 10, 75, 23));
        groupGraph = new QGroupBox(centralWidget);
        groupGraph->setObjectName(QStringLiteral("groupGraph"));
        groupGraph->setEnabled(true);
        groupGraph->setGeometry(QRect(10, 390, 311, 141));
        label_graph = new QLabel(groupGraph);
        label_graph->setObjectName(QStringLiteral("label_graph"));
        label_graph->setGeometry(QRect(10, 20, 61, 20));
        comboGraph = new QComboBox(groupGraph);
        comboGraph->setObjectName(QStringLiteral("comboGraph"));
        comboGraph->setGeometry(QRect(80, 20, 101, 22));
        graphicsGraph = new QGraphicsView(groupGraph);
        graphicsGraph->setObjectName(QStringLiteral("graphicsGraph"));
        graphicsGraph->setGeometry(QRect(10, 50, 291, 81));
        labelLog = new QLabel(centralWidget);
        labelLog->setObjectName(QStringLiteral("labelLog"));
        labelLog->setGeometry(QRect(20, 540, 931, 20));
        label_3 = new QLabel(centralWidget);
        label_3->setObjectName(QStringLiteral("label_3"));
        label_3->setGeometry(QRect(190, 20, 91, 16));
        label_4 = new QLabel(centralWidget);
        label_4->setObjectName(QStringLiteral("label_4"));
        label_4->setGeometry(QRect(300, 13, 101, 20));
        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 430, 20));
        menuPogoda = new QMenu(menuBar);
        menuPogoda->setObjectName(QStringLiteral("menuPogoda"));
        menuPomoc = new QMenu(menuBar);
        menuPomoc->setObjectName(QStringLiteral("menuPomoc"));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MainWindow->setStatusBar(statusBar);

        menuBar->addAction(menuPogoda->menuAction());
        menuBar->addAction(menuPomoc->menuAction());
        menuPogoda->addAction(actionUstawienia_programu);
        menuPogoda->addAction(actionWyj_cie);
        menuPomoc->addAction(actionO_programie);

        retranslateUi(MainWindow);

        tabMapType->setCurrentIndex(1);


        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "Pogoda", 0));
#ifndef QT_NO_TOOLTIP
        MainWindow->setToolTip(QString());
#endif // QT_NO_TOOLTIP
        actionUstawienia_programu->setText(QApplication::translate("MainWindow", "Ustawienia programu", 0));
        actionO_programie->setText(QApplication::translate("MainWindow", "O programie", 0));
        actionWyj_cie->setText(QApplication::translate("MainWindow", "Wyj\305\233cie", 0));
        bLayerUp->setText(QApplication::translate("MainWindow", "\342\226\262", 0));
        bLayerDown->setText(QApplication::translate("MainWindow", "\342\226\274", 0));
        bLayerNew->setText(QApplication::translate("MainWindow", "Nowa warstwa", 0));
        bLayerVisibility->setText(QApplication::translate("MainWindow", "Widoczno\305\233\304\207", 0));
        bLayerDelete->setText(QApplication::translate("MainWindow", "Usu\305\204 warstw\304\231", 0));
        QTreeWidgetItem *___qtreewidgetitem = treeWidget->headerItem();
        ___qtreewidgetitem->setText(0, QApplication::translate("MainWindow", "Warstwy", 0));
        tabMapType->setTabText(tabMapType->indexOf(tab_gdal), QApplication::translate("MainWindow", "GDAL", 0));
        pushButton->setText(QApplication::translate("MainWindow", "pobierz map\304\231", 0));
        label_5->setText(QApplication::translate("MainWindow", "lon:", 0));
        label_6->setText(QApplication::translate("MainWindow", "lat:", 0));
        tabMapType->setTabText(tabMapType->indexOf(tab_osm), QApplication::translate("MainWindow", "OpenStreetMap", 0));
        label_MapType->setText(QApplication::translate("MainWindow", "Wy\305\233wietlana mapa:", 0));
        bNavUp->setText(QApplication::translate("MainWindow", "\342\226\262", 0));
        bNavDown->setText(QApplication::translate("MainWindow", "\342\226\274", 0));
        bNavRight->setText(QApplication::translate("MainWindow", "\342\226\272", 0));
        bNavLeft->setText(QApplication::translate("MainWindow", "\342\227\204", 0));
        label_textScale->setText(QApplication::translate("MainWindow", "Zoom:", 0));
        labelScale->setText(QString());
        bNavUp_2->setText(QApplication::translate("MainWindow", "+", 0));
        bNavUp_3->setText(QApplication::translate("MainWindow", "-", 0));
        groupWeather->setTitle(QApplication::translate("MainWindow", "Ustawienia pogody", 0));
        label_hour->setText(QApplication::translate("MainWindow", "Godzina:", 0));
        label_date->setText(QApplication::translate("MainWindow", "Data:", 0));
        checkBox->setText(QApplication::translate("MainWindow", "Tryb zaawansowany", 0));
        groupAdvanced->setTitle(QString());
        label_param->setText(QApplication::translate("MainWindow", "Parametr:", 0));
        checkFilter->setText(QApplication::translate("MainWindow", "Filtr", 0));
        label_color->setText(QApplication::translate("MainWindow", "Kolory:", 0));
        bColor1->setText(QString());
        bColor2->setText(QString());
        groupFilter->setTitle(QString());
        label->setText(QApplication::translate("MainWindow", ">", 0));
        label_2->setText(QApplication::translate("MainWindow", "<", 0));
        bShowWeather->setText(QApplication::translate("MainWindow", "Wy\305\233wietl", 0));
        groupGraph->setTitle(QApplication::translate("MainWindow", "Przebieg wybranego parametru w czasie", 0));
        label_graph->setText(QApplication::translate("MainWindow", "Okres czasu:", 0));
        labelLog->setText(QApplication::translate("MainWindow", "Wsp\303\263\305\202rz\304\231dne: xxxxxxxxx N, xxxxxxxxxxxx E;   Temperatura: 21oC, Wilgotno\305\233\304\207 powietrza: 40%, Opady: brak, Pr\304\231dko\305\233\304\207 wiatru: 25km/h, Kierunek: NE", 0));
        label_3->setText(QApplication::translate("MainWindow", "TextLabel", 0));
        label_4->setText(QApplication::translate("MainWindow", "TextLabel", 0));
        menuPogoda->setTitle(QApplication::translate("MainWindow", "Opcje", 0));
        menuPomoc->setTitle(QApplication::translate("MainWindow", "Pomoc", 0));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
