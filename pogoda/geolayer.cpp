#include "geolayer.h"

GeoLayer::GeoLayer(QImage* img, int proj, point corLU, point corRB, QObject *parent) : QObject(parent)
{
    image = img->copy();
    projection = proj;
    cornerLU = corLU;
    cornerRB = corRB;
    xInc = (cornerRB.x - cornerLU.x)/(double)image.size().width();
    yInc = (cornerLU.y - cornerRB.y)/(double)image.size().height();
    visibility=false;
    //qDebug() << "Created GeoLayer with parameters:" << image.height() << image.width() << cornerLU.x << cornerLU.y << cornerRB.x << cornerRB.y;
}

GeoLayer::~GeoLayer() { }

int GeoLayer::getImgHeight()
{
    return image.height();
}

QImage GeoLayer::getImage()
{
    return image;
}

QColor GeoLayer::getPixel(double lat, double lon)
{
    QColor color = QColor(0, 0, 0, 0);
    if (lat < cornerRB.x && lat > cornerLU.x)
    {
        if (lon > cornerRB.y && lon < cornerLU.y)
        {
            //calculate pixel position
            point pixPos;
            switch (projection)
            {
            case 1:
            {
                pixPos.x = ((lat - cornerLU.x) / xInc);
                pixPos.y = ((cornerLU.y - lon) / yInc);
                //qDebug() << "Getting info for pixel" << pixPos.x << " " << pixPos.y;
                QRgb rgbColor = image.pixel((int)pixPos.x, (int)pixPos.y);
                color = QColor(rgbColor);
                return color;
            }
                break;
            }
        }
    }
    return color;
}
void GeoLayer::setImage(QImage img)
{
    image=img.copy();
}
void GeoLayer::setCorners(point corLU, point corRB)
{
    cornerLU = corLU;
    cornerRB = corRB;
}
