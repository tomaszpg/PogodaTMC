#include "viewport.h"
#include <QDebug>
#include <math.h>

#define deg2rad(d) (((d)*M_PI)/180)
#define rad2deg(d) (((d)*180)/M_PI)
#define earth_radius 6378137

double y2lat_d(double y) { return rad2deg(2 * atan(exp(  deg2rad(y) ) ) - M_PI/2); }
double x2lon_d(double x) { return x; }
double lat2y_d(double lat) { return rad2deg(log(tan(M_PI/4+ deg2rad(lat)/2))); }
double lon2x_d(double lon) { return lon; }
double addLat(double current, double inc) { return y2lat_d(lat2y_d(current) + inc); }

Viewport::Viewport(int sizeX_init, int sizeY_init, QObject *parent) : QObject(parent)
{
    sizeX = sizeX_init;
    sizeY = sizeY_init;
    center.x = 19.45;
    center.y = 51.9574;
    cornerMaxLU.x = 19.45 - 5.625;
    cornerMaxRB.x = 19.45 + 5.625;
    cornerMaxLU.y = y2lat_d(lat2y_d(48.5) + 11.25);
    cornerMaxRB.y = 48.5;
    cornerLU = cornerMaxLU;
    cornerRB = cornerMaxRB;
    currentZoom = 0;
    zoom = new double[5];
    zoom[0] = 11.25;
    zoom[1] = 5.625;
    zoom[2] = 2.813;
    zoom[3] = 1.406;
    zoom[4] = 0.703;
    incX = (cornerMaxRB.x - cornerMaxLU.x) / 512;
    incY = (cornerMaxLU.y - cornerMaxRB.y) / 512;
    image = new QImage (512, 512, QImage::Format_RGB32);
    image->fill(Qt::black);
}


QImage Viewport::draw(GeoLayer *&layer, int a = 255)
{
    double range = lat2y_d(cornerLU.y) - lat2y_d(cornerRB.y);
    for (int i = 0; i < 512; i++)
    {
        double lat = cornerLU.x + (i * incX);
        for (int j = 0; j < 512; j++)
        {
            double lon = ((lat2y_d(cornerLU.y - (j * incY)) - lat2y_d(cornerRB.y))/range) * (cornerLU.y - cornerRB.y) + cornerRB.y;
            double opacity = double(a) / 255.0;
            //double lon = cornerLU.y - (j * incY);
            QColor colorA = layer->getPixel(lat, lon);
            if (colorA.alpha() != 0)
            {
                QColor colorB = QColor(image->pixel(i, j));
                QColor colorFinal = QColor(
                            (colorA.red() * opacity) + (colorB.red() * (1-opacity)),
                            (colorA.green() * opacity) + (colorB.green() * (1-opacity)),
                            (colorA.blue() * opacity) + (colorB.blue() * (1-opacity)),
                            255
                            );
                image->setPixel(i, j, colorFinal.rgb());
            }
        }
    }
    return *image;
}


GeoLayer::point Viewport::getLatLon(QPoint point)
{
    double range = lat2y_d(cornerLU.y) - lat2y_d(cornerRB.y);
    GeoLayer::point latLonPoint;
    latLonPoint.x = cornerLU.x + (point.x() * incX);
    latLonPoint.y = ((lat2y_d(cornerLU.y - (point.y() * incY)) - lat2y_d(cornerRB.y))/range) * (cornerLU.y - cornerRB.y) + cornerRB.y;
    qDebug() << "Point:" << latLonPoint.x << latLonPoint.y;
    return latLonPoint;
}

void Viewport::clear()
{
    image->fill(Qt::black);
}

void Viewport::moveTo(GeoLayer::point point)
{
    cornerLU.x = point.x;
    cornerLU.y = point.y;
    cornerRB.x = point.x + zoom[currentZoom];
    cornerRB.y = y2lat_d(lat2y_d(point.y) - zoom[currentZoom]);
    incX = (cornerRB.x - cornerLU.x) / 512;
    incY = (cornerLU.y - cornerRB.y) / 512;
    //qDebug() << "New size:" << cornerRB.x - cornerLU.x << cornerLU.y - cornerRB.y;
}

void Viewport::scaleDown()
{
    if (currentZoom != 4) // aktualnie nie w skali minimalnej
    {
        //qDebug() << "Starting from:" << cornerLU.x << cornerLU.y;
        currentZoom++;
        cornerLU.x += (0.5 * zoom[currentZoom]);
        cornerLU.y = addLat(cornerLU.y, -(0.5 * zoom[currentZoom]));
        //qDebug() << "Moving to:" << cornerLU.x << cornerLU.y;
        moveTo(cornerLU);
    }
}

void Viewport::scaleUp()
{
    if (currentZoom != 0) // aktualnie nie w skali maksymalnej
    {
        //qDebug() << "Starting from:" << cornerLU.x << cornerLU.y;
        // wstepne okreslenie pozycji wierzcholka
        cornerLU.x -= (0.5 * zoom[currentZoom]);
        cornerLU.y = addLat(cornerLU.y, (0.5 * zoom[currentZoom]));
        //qDebug() << "Pre-fix:" << cornerLU.x << cornerLU.y;
        currentZoom--;
        // korekta (jesli wymagana)
        if (cornerLU.x < cornerMaxLU.x)
            cornerLU.x = cornerMaxLU.x;
        if (cornerLU.y > cornerMaxLU.y)
            cornerLU.y = cornerMaxLU.y;
        if ((cornerLU.x + zoom[currentZoom]) > cornerMaxRB.x)
            cornerLU.x = cornerMaxRB.x - zoom[currentZoom];
        if (addLat(cornerLU.y, -zoom[currentZoom]) < cornerMaxRB.y)
            cornerLU.y = addLat(cornerMaxRB.y, zoom[currentZoom]);
        moveTo(cornerLU);
        //qDebug() << "Post-fix:" << cornerLU.x << cornerLU.y;
    }
}

void Viewport::moveUp()
{
    if (addLat(cornerLU.y, (0.5 * zoom[currentZoom])) > cornerMaxLU.y)
    {
        // poza zakresem, przejdz do granicy
        cornerLU.y = cornerMaxLU.y;
        moveTo(cornerLU);
    }
    else
    {
        // w zakresie, przejdz do obliczonego punktu
        cornerLU.y = addLat(cornerLU.y, (0.5 * zoom[currentZoom]));
        moveTo(cornerLU);
    }
}

void Viewport::moveDown()
{
    if (addLat(cornerLU.y, (-1.5 * zoom[currentZoom])) < cornerMaxRB.y)
    {
        // poza zakresem, przejdz do granicy
        cornerLU.y = addLat(cornerMaxRB.y, zoom[currentZoom]);
        moveTo(cornerLU);
    }
    else
    {
        // w zakresie, przejdz do obliczonego punktu
        cornerLU.y = addLat(cornerLU.y, (-0.5 * zoom[currentZoom]));
        moveTo(cornerLU);
    }
}

void Viewport::moveLeft()
{
    if ((cornerLU.x - (0.5 * zoom[currentZoom])) < cornerMaxLU.x)
    {
        // poza zakresem, przejdz do granicy
        cornerLU.x = cornerMaxLU.x;
        moveTo(cornerLU);
    }
    else
    {
        // w zakresie, przejdz do obliczonego punktu
        cornerLU.x = cornerLU.x - (0.5 * zoom[currentZoom]);
        moveTo(cornerLU);
    }
}

void Viewport::moveRight()
{
    if ((cornerLU.x + (1.5 * zoom[currentZoom])) > cornerMaxRB.x)
    {
        // poza zakresem, przejdz do granicy
        cornerLU.x = cornerMaxRB.x - zoom[currentZoom];
        moveTo(cornerLU);
    }
    else
    {
        // w zakresie, przejdz do obliczonego punktu
        cornerLU.x = cornerLU.x + (0.5 * zoom[currentZoom]);
        moveTo(cornerLU);
    }
}

Viewport::~Viewport() { }


