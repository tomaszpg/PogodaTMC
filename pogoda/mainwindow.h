#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "filedownloader.h"
#include "geolayer.h"
#include "viewport.h"
#include <QTreeWidgetItem>
#include "mapwindow.h"
#include "minimap.h"
#include "settingsdialog.h"
namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow(); 

private:
    Ui::MainWindow *ui;
    bool advancedMode;
    FileDownloader *m_pFileCtrl;
    FileDownloader *n_pFileCtrl;
    FileDownloader *osm_pFileCtrl;
    QColor colorMin;
    QColor colorMax;
    //GeoLayer *weatherLayer;
    Viewport *vPort;
    double* wMetaData;
    GeoLayer::point pointPos;
    int wSizeX;
    int wSizeY;
    int layerNum;
    int layerNum_osm;
    QVector<GeoLayer*> *layers;
    QVector<GeoLayer*> *layers_osm;
    MapWindow *map;
    MiniMap *miniMap;
    double zoom;
    SettingsDialog *settings;
    bool flaga;

private slots:
    void setupGUI();
    void logPrint(QString text);
    void setColors();
    void dlWMetaData();
    void setWMetaData();
    double lat2y_d(double lat);
    double y2lat_d(double lat);

    void on_checkBox_clicked(bool checked);
    void on_checkFilter_clicked(bool checked);
    void on_bShowWeather_clicked();
    void processFile();
    void showPosition();
    void updateSettings();
    QString parseUrl(QString url);
    void on_bColor1_clicked();
    void on_bColor2_clicked();
    void on_bNavUp_2_clicked();
    void on_bNavUp_3_clicked();
    void on_bNavUp_clicked();
    void on_bNavDown_clicked();
    void on_bNavRight_clicked();
    void on_bNavLeft_clicked();
    void on_bLayerNew_clicked();
    void on_bLayerDelete_clicked();
    void on_bLayerUp_clicked();
    void on_bLayerDown_clicked();
    void on_treeWidget_itemClicked(QTreeWidgetItem *item, int column);
    void on_bLayerVisibility_clicked();

    void on_pushButton_clicked();
    void show_url_image();

    void on_actionUstawienia_programu_triggered();

    void on_bLayerVisibility_2_clicked();

    void on_bLayerUp_2_clicked();

    void on_bLayerDown_2_clicked();

    void on_tabMapType_currentChanged(int index);

    void on_bLayerDelete_2_clicked();

public slots:
    void refreshView();

};

#endif // MAINWINDOW_H
