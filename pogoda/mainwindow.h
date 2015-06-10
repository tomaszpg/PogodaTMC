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
    bool fileChanged;
    QVector<FileDownloader *> * osm_pFileCtrl;
    FileDownloader *m_pFileCtrl;
    FileDownloader *n_pFileCtrl;
    //FileDownloader *osm_pFileCtrl;
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
    int aktualX;
    int aktualY;
    double *zoom_levels;
    int temp_size;
    double *tabX;
    double *tabY;
private slots:
    void setupGUI();
    void logPrint(QString text);
    void setColors();
    void dlWMetaData();
    void setWMetaData(int num);
    double lat2y_d(double lat);
    double y2lat_d(double lat);

    void on_checkFilter_clicked(bool checked);
    void on_bShowWeather_clicked();
    void processFile(int num);
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
    void show_url_image(int num=NULL);

    void on_actionUstawienia_programu_triggered();

    void on_tabMapType_currentChanged(int index);

    void on_b_showIcons_clicked();

    void on_actionWyj_cie_triggered();

    void on_actionMapa_triggered();

    void on_actionMinimapa_triggered();

    void on_actionO_programie_triggered();

    void on_comboHour_currentIndexChanged(int index);

    void on_calendarWidget_selectionChanged();

public slots:
    void refreshView();

};

#endif // MAINWINDOW_H
