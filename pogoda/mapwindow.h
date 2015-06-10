#ifndef MAPWINDOW_H
#define MAPWINDOW_H

#include <QDialog>
#include "viewport.h"
#include <QImage>
#include "clickablelabel.h"
#include "filedownloader.h"

namespace Ui {
class MapWindow;
}

class MapWindow : public QDialog
{
    Q_OBJECT

public:
    explicit MapWindow(QWidget *parent = 0);
    ~MapWindow();

private:
    Ui::MapWindow *ui;
    Viewport *vPort;
    QObject myParent;
    QImage numberImg[12];
    FileDownloader *temp_pFileCtrl;
    FileDownloader *cloud_pFileCtrl;
    FileDownloader *rain_pFileCtrl;
    float **tempGrid;
    float **cloudGrid;
    float **rainGrid;
    int layersDone;
    QImage imgCopy;

public slots:
    Viewport * getHandle();
    void drawImage(QImage image);
    clickableLabel * getLabel();
    void updateGradient(float min, float max, QString text, QColor colorMin, QColor colorMax);
    void placeIcon(float x, float y);
    void getLayers(QString tempUrl, QString cloudUrl, QString rainUrl);

private slots:
    void resizeEvent(QResizeEvent *);
    void resizeMap(int w, int h);
    void processTempFile(int num);
    void processCloudFile(int num);
    void processRainFile(int num);
    void checkLayersDone();
    void drawIcons();
    QString getIcon(double lat, double lon, int *temp);

signals:
    void resizeSignal();
};

#endif // MAPWINDOW_H
