#ifndef VIEWPORT
#define VIEWPORT

#include <QObject>
#include <QImage>
#include <QColor>
#include "geolayer.h"

class Viewport : public QObject
{
    Q_OBJECT
private:
    QImage *image;
    int sizeX;
    int sizeY;

    double* zoom;
    double incX;
    double incY;
    int currentZoom;

public:
    GeoLayer::point cornerLU;
    GeoLayer::point cornerRB;
    GeoLayer::point cornerMaxLU;
    GeoLayer::point cornerMaxRB;
    GeoLayer::point center;
    explicit Viewport(int sizeX_init, int sizeY_init, QObject *parent = 0);
    virtual ~Viewport();
    QImage draw(GeoLayer*& layer, int a);
    void clear();
    void moveTo(GeoLayer::point point);
    void goToMinimapPos(int x, int y);
    void moveLeft();
    void moveRight();
    void moveUp();
    void moveDown();
    void scaleUp();
    void scaleDown();
    void resize(int w, int h);
    GeoLayer::point getLatLon(QPoint point);
    void getBoundingBox(int *leftUpperX, int *leftUpperY, int *rightBottomX, int *rightBootomY);

signals:
    void refresh();
};

#endif // VIEWPORT
