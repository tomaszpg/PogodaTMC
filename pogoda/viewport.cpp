#define _USE_MATH_DEFINES
#include "viewport.h"
#include <QDebug>
#include <math.h>
#include <geolayer.h>
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
    incX = (cornerMaxRB.x - cornerMaxLU.x) / sizeX;
    incY = (cornerMaxLU.y - cornerMaxRB.y) / sizeY;
    currentZoom = 0;
    /*zoomX = new double[5];
    zoomY = new double[5];
    zoomX[0] = cornerMaxRB.x-cornerMaxLU.x;
    zoomY[0] = cornerMaxLU.y-cornerMaxRB.y;
    for(int i=1;i<5;i++)
    {
        zoomX[i]=zoomX[i-1]/2.0;
        zoomY[i]=zoomY[i-1]/2.0;
    }*/
    zoom = new double[5];
    zoom[0] = cornerMaxRB.x-cornerMaxLU.x;
    for(int i=1;i<5;i++)
    {
        zoom[i]=zoom[i-1]/2.0;
    }
    /*zoom[1] = 5.625;
    zoom[2] = 2.813;
    zoom[3] = 1.406;
    zoom[4] = 0.703;*/
    image = new QImage (sizeX, sizeY, QImage::Format_RGB32);
    image->fill(Qt::black);
}


QImage Viewport::draw(GeoLayer *&layer, int a = 255)
{
    double range = lat2y_d(cornerLU.y) - lat2y_d(cornerRB.y);
    for (int i = 0; i < sizeX; i++)
    {
        double lat = cornerLU.x + (i * incX);
        for (int j = 0; j < sizeY; j++)
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

void Viewport::resize(int w, int h)
{
    sizeX = w;
    sizeY = h;
    incX = (cornerRB.x - cornerLU.x) / sizeX;
    incY = (cornerLU.y - cornerRB.y) / sizeY;
    image = new QImage (w, h, QImage::Format_RGB32);
    //qDebug() << "Resized to" << w << "," << h;
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
    incX = (cornerRB.x - cornerLU.x) / sizeX;
    incY = (cornerLU.y - cornerRB.y) / sizeY;
    //qDebug() << "New size:" << cornerRB.x - cornerLU.x << cornerLU.y - cornerRB.y;
    /*cornerLU.x = point.x;
    cornerLU.y = point.y;
    //cornerRB.x = point.x + zoomX[currentZoom];
    cornerRB.y = y2lat_d(lat2y_d(point.y) - zoomY[currentZoom]);
    cornerRB.y =point.y- zoomY[currentZoom];
    incX = (cornerRB.x - cornerLU.x) / sizeX;
    incY = (cornerLU.y - cornerRB.y) / sizeY;*/
}

void Viewport::goToMinimapPos(int x, int y)
{

    cornerLU.x = cornerMaxLU.x + zoom[0] * (float)x/256 - 0.5 * zoom[currentZoom];
    cornerLU.y = y2lat_d(lat2y_d(cornerMaxLU.y) - zoom[0] * (float)y/256 + 0.5 * zoom[currentZoom]);

    // prawy zakres
    if (cornerLU.x + zoom[currentZoom] > cornerMaxRB.x)
        cornerLU.x = cornerMaxRB.x - zoom[currentZoom];

    // lewy zakres
    if (cornerLU.x < cornerMaxLU.x)
        cornerLU.x = cornerMaxLU.x;

    // gorny zakres
    if (cornerLU.y > cornerMaxLU.y)
        cornerLU.y = cornerMaxLU.y;

    // dolny zakres
    if (y2lat_d(lat2y_d(cornerLU.y) - zoom[currentZoom]) < cornerMaxRB.y)
        cornerLU.y = y2lat_d(lat2y_d(cornerMaxRB.y) + zoom[currentZoom]);

    moveTo(cornerLU);
    emit refresh();
    /*cornerLU.x = cornerMaxLU.x + zoomX[0] * (float)x/256 - 0.5 * zoomX[currentZoom];
    cornerLU.y = y2lat_d(lat2y_d(cornerMaxLU.y) - zoomY[0] * (float)y/256 + 0.5 * zoomY[currentZoom]);

    // prawy zakres
    if (cornerLU.x + zoomX[currentZoom] > cornerMaxRB.x)
        cornerLU.x = cornerMaxRB.x - zoomX[currentZoom];

    // lewy zakres
    if (cornerLU.x < cornerMaxLU.x)
        cornerLU.x = cornerMaxLU.x;

    // gorny zakres
    if (cornerLU.y > cornerMaxLU.y)
        cornerLU.y = cornerMaxLU.y;

    // dolny zakres
    if (y2lat_d(lat2y_d(cornerLU.y) - zoomY[currentZoom]) < cornerMaxRB.y)
        cornerLU.y = y2lat_d(lat2y_d(cornerMaxRB.y) + zoomY[currentZoom]);

    moveTo(cornerLU);
    emit refresh();*/
}

void Viewport::getBoundingBox(int *leftUpperX, int *leftUpperY, int *rightBottomX, int *rightBootomY)
{
    double range = lat2y_d(cornerMaxLU.y) - lat2y_d(cornerMaxRB.y);
    *leftUpperX = (int)((cornerLU.x - cornerMaxLU.x)/zoom[0] * 255);
    *rightBottomX = (int)((cornerLU.x - cornerMaxLU.x + zoom[currentZoom])/zoom[0] * 255);
    *leftUpperY = (int)((lat2y_d(cornerMaxLU.y) - lat2y_d(cornerLU.y))/range * 255);
    *rightBootomY = (int)((lat2y_d(cornerMaxLU.y) - lat2y_d(cornerLU.y) + zoom[currentZoom])/range * 255);
    /*double range = lat2y_d(cornerMaxLU.y) - lat2y_d(cornerMaxRB.y);
    *leftUpperX = (int)((cornerLU.x - cornerMaxLU.x)/zoomX[0] * 255);
    *rightBottomX = (int)((cornerLU.x - cornerMaxLU.x + zoomX[currentZoom])/zoomX[0] * 255);
    *leftUpperY = (int)((lat2y_d(cornerMaxLU.y) - lat2y_d(cornerLU.y))/zoomY[0] * 255);
    *rightBootomY = (int)((lat2y_d(cornerMaxLU.y) - lat2y_d(cornerLU.y) + zoomY[currentZoom])/zoomY[0] * 255);*/
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
    /*if (currentZoom != 4) // aktualnie nie w skali minimalnej
    {
        //qDebug() << "Starting from:" << cornerLU.x << cornerLU.y;
        currentZoom++;
        cornerLU.x += (0.5 * zoomX[currentZoom]);
        cornerLU.y = addLat(cornerLU.y, -(0.5 * zoomY[currentZoom]));
        //qDebug() << "Moving to:" << cornerLU.x << cornerLU.y;
        moveTo(cornerLU);
    }*/
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
        /*
        //qDebug() << "Post-fix:" << cornerLU.x << cornerLU.y;
        cornerLU.x -= (0.5 * zoomX[currentZoom]);
        cornerLU.y = addLat(cornerLU.y, (0.5 * zoomY[currentZoom]));
        //qDebug() << "Pre-fix:" << cornerLU.x << cornerLU.y;
        currentZoom--;
        // korekta (jesli wymagana)
        if (cornerLU.x < cornerMaxLU.x)
            cornerLU.x = cornerMaxLU.x;
        if (cornerLU.y > cornerMaxLU.y)
            cornerLU.y = cornerMaxLU.y;
        if ((cornerLU.x + zoomX[currentZoom]) > cornerMaxRB.x)
            cornerLU.x = cornerMaxRB.x - zoomX[currentZoom];
        if (addLat(cornerLU.y, -zoomY[currentZoom]) < cornerMaxRB.y)
            cornerLU.y = addLat(cornerMaxRB.y, zoomY[currentZoom]);
        moveTo(cornerLU);*/
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
    /*if (addLat(cornerLU.y, (0.5 * zoomY[currentZoom])) > cornerMaxLU.y)
    {
        // poza zakresem, przejdz do granicy
        cornerLU.y = cornerMaxLU.y;
        moveTo(cornerLU);
    }
    else
    {
        // w zakresie, przejdz do obliczonego punktu
        cornerLU.y = addLat(cornerLU.y, (0.5 * zoomY[currentZoom]));
        moveTo(cornerLU);
    }*/
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
    /*if (addLat(cornerLU.y, (-1.5 * zoomY[currentZoom])) < cornerMaxRB.y)
    {
        // poza zakresem, przejdz do granicy
        cornerLU.y = addLat(cornerMaxRB.y, zoomY[currentZoom]);
        moveTo(cornerLU);
    }
    else
    {
        // w zakresie, przejdz do obliczonego punktu
        cornerLU.y = addLat(cornerLU.y, (-0.5 * zoomY[currentZoom]));
        moveTo(cornerLU);
    }*/
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
    /*if ((cornerLU.x - (0.5 * zoomX[currentZoom])) < cornerMaxLU.x)
    {
        // poza zakresem, przejdz do granicy
        cornerLU.x = cornerMaxLU.x;
        moveTo(cornerLU);
    }
    else
    {
        // w zakresie, przejdz do obliczonego punktu
        cornerLU.x = cornerLU.x - (0.5 * zoomX[currentZoom]);
        moveTo(cornerLU);
    }*/
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
    /*if ((cornerLU.x + (1.5 * zoomX[currentZoom])) > cornerMaxRB.x)
    {
        // poza zakresem, przejdz do granicy
        cornerLU.x = cornerMaxRB.x - zoomX[currentZoom];
        moveTo(cornerLU);
    }
    else
    {
        // w zakresie, przejdz do obliczonego punktu
        cornerLU.x = cornerLU.x + (0.5 * zoomX[currentZoom]);
        moveTo(cornerLU);
    }*/
}

void Viewport::setCorners(GeoLayer::point cornerLU_init, GeoLayer::point cornerRB_init)
{
    cornerMaxLU.x = cornerLU_init.x;
    cornerMaxRB.x = cornerRB_init.x;
    cornerMaxLU.y = cornerLU_init.y;
    cornerMaxRB.y = cornerRB_init.y;
    cornerLU = cornerMaxLU;
    cornerRB = cornerMaxRB;
    incX = (cornerMaxRB.x - cornerMaxLU.x) / sizeX;
    incY = (cornerMaxLU.y - cornerMaxRB.y) / sizeY;
    /*zoomX[0] = cornerMaxRB.x-cornerMaxLU.x;
    zoomY[0] = cornerMaxLU.y-cornerMaxRB.y;
    for(int i=1;i<5;i++)
    {
        zoomX[i]=zoomX[i-1]/2;
        zoomY[i]=zoomY[i-1]/2;
    }*/
    zoom = new double[5];
    zoom[0] = cornerMaxRB.x-cornerMaxLU.x;
    for(int i=1;i<5;i++)
    {
        zoom[i]=zoom[i-1]/2.0;
    }
}

Viewport::~Viewport() { }


