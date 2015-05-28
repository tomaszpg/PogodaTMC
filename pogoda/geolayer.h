#ifndef GEOLAYER_H
#define GEOLAYER_H

#include <QObject>
#include <QImage>
#include <QColor>
#include <QDebug>

class GeoLayer : public QObject
{
    Q_OBJECT
private:
    QImage image;
    double xInc;
    double yInc;
    int projection;

public:
    struct point
        {
            double x;
            double y;
        };
    explicit GeoLayer(QImage* image, int proj, point corLU, point corBR, QObject *parent = 0);
    virtual ~GeoLayer();
    point cornerLU;
    point cornerRB;
    bool visibility;
    QColor getPixel (double lat, double lon);
    int getImgHeight();
    QImage getImage();
    void setImage(QImage img);
    void setCorners(point corLU, point corBR);
};

#endif // GEOLAYER_H
