#include "mapwindow.h"
#include "ui_mapwindow.h"
#include <QDir>
#include <QFileInfo>
#include <QPainter>
#include <QMessageBox>
#include "geolayer.h"


bool imgFileExists(QString path) {
    QFileInfo checkFile(path);
    // check if file exists and if yes: Is it really a file and no directory?
    if (checkFile.exists() && checkFile.isFile()) {
        return true;
    } else {
        return false;
    }
}

MapWindow::MapWindow(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::MapWindow)
{
    ui->setupUi(this);
    vPort = new Viewport(512, 512, this);

    tempGrid = new float*[170];
    cloudGrid = new float*[170];
    rainGrid = new float*[170];

    for(int i = 0; i < 170; ++i)
    {
        tempGrid[i] = new float[325];
        cloudGrid[i] = new float[325];
        rainGrid[i] = new float[325];
    }

    layersDone = 0;

    for (int i = 0; i < 12; i++)
    {
        QString path = QDir::currentPath() + QString("/icons/numbers/n%1.png").arg(i);
        if (imgFileExists(path))
        {
           numberImg[i] = QImage(path);
        }
        else
        {
            qDebug() << "Plik " << path << " nie istnieje.";
        }
    }
}

MapWindow::~MapWindow()
{
    delete ui;
}

Viewport * MapWindow::getHandle()
{
    return vPort;
}

void MapWindow::drawImage(QImage image)
{
    //placeIcon(&image, "clouds", 17, 0.5, 0.5);
    //imgPointer = &image;
    imgCopy = QImage(image);
    ui->label->setPixmap(QPixmap::fromImage(image));
    ui->label->show();
}

void MapWindow::resizeEvent(QResizeEvent * /*resizeEvent*/)
{
    int h = this->size().height();
    int w = this->size().width();
    if (h > w)
    {
        this->resize(w, w);
        resizeMap(w, w);
    }

    else
    {
        this->resize(h, h);
        resizeMap(h, h);
    }
}

void MapWindow::getLayers(QString tempUrl, QString cloudUrl, QString rainUrl)
{
    if (QString::compare(tempUrl, "OLD", Qt::CaseSensitive))
    {
        layersDone = 0;
        temp_pFileCtrl = new FileDownloader(QUrl(tempUrl),0, this);
        connect(temp_pFileCtrl, SIGNAL (downloaded(int)), this, SLOT (processTempFile(int)));
        cloud_pFileCtrl = new FileDownloader(QUrl(cloudUrl),0, this);
        connect(cloud_pFileCtrl, SIGNAL (downloaded(int)), this, SLOT (processCloudFile(int)));
        rain_pFileCtrl = new FileDownloader(QUrl(rainUrl),0, this);
        connect(rain_pFileCtrl, SIGNAL (downloaded(int)), this, SLOT (processRainFile(int)));
    }
    else
        checkLayersDone();
}

void MapWindow::checkLayersDone()
{
    if (layersDone != 3)
        layersDone++;
    if (layersDone == 3)
    {
        drawIcons();
        //layersDone = 0;
    }
}

void MapWindow::processTempFile(int num)
{
    if (!temp_pFileCtrl->downloadedData().isNull())
    {
        QString data = (temp_pFileCtrl->downloadedData());
        QRegExp rx("(\\ |\\,|\\t|\\n)");
        QStringList query = data.split(rx);
        query.removeAll(NULL);
        if (query.size() == 325*170)
        {
            //QRegExp re("\\d*");
            for (int i = 0; i < 170; i++)
            {
                for (int j = 0; j < 325; j++)
                {
                    tempGrid[i][j] = query[(170-i-1)*325 + j].toFloat() - 273.15;
                }
            }
            qDebug() << "Temp OK";
            checkLayersDone();
        }
        else
            QMessageBox::information(
                this,
                tr("Błąd"),
                tr("Nie udało się wczytać pliku temperatury.") );
    }
    else
    {
        QMessageBox::information(
            this,
            tr("Błąd"),
            tr("Nie udało się wczytać pliku temperatury.") );
    }
}

void MapWindow::processCloudFile(int num)
{
    if (!cloud_pFileCtrl->downloadedData().isNull())
    {
        QString data = (cloud_pFileCtrl->downloadedData());
        QRegExp rx("(\\ |\\,|\\t|\\n)");
        QStringList query = data.split(rx);
        query.removeAll(NULL);
        if (query.size() == 325*170)
        {
            //QRegExp re("\\d*");
            for (int i = 0; i < 170; i++)
            {
                for (int j = 0; j < 325; j++)
                {
                    cloudGrid[i][j] = query[(170-i-1)*325 + j].toFloat();
                }
            }
            //qDebug() << "Clouds OK";
            checkLayersDone();
        }
        else
            QMessageBox::information(
                this,
                tr("Błąd"),
                tr("Nie udało się wczytać pliku zachmurzenia.") );
    }
    else
    {
        QMessageBox::information(
            this,
            tr("Błąd"),
            tr("Nie udało się wczytać pliku zachmurzenia.") );
    }
}

void MapWindow::processRainFile(int num)
{
    if (!rain_pFileCtrl->downloadedData().isNull())
    {
        QString data = (rain_pFileCtrl->downloadedData());
        QRegExp rx("(\\ |\\,|\\t|\\n)");
        QStringList query = data.split(rx);
        query.removeAll(NULL);
        if (query.size() == 325*170)
        {
            //QRegExp re("\\d*");
            for (int i = 0; i < 170; i++)
            {
                for (int j = 0; j < 325; j++)
                {
                    rainGrid[i][j] = query[(170-i-1)*325 + j].toFloat();
                }
            }
            //qDebug() << "Rain OK";
            checkLayersDone();
        }
        else
            QMessageBox::information(
                this,
                tr("Błąd"),
                tr("Nie udało się wczytać pliku opadów.") );
    }
    else
    {
        QMessageBox::information(
            this,
            tr("Błąd"),
            tr("Nie udało się wczytać pliku opadów.") );
    }
}

QString MapWindow::getIcon(double lat, double lon, int *temp)
{
    //qDebug() << "Name requested for lat:" << lat << "lon:" << lon;
    float xInc = 0.0378444945891919;
    float yInc = 0.0378444945891919;
    GeoLayer::point cornerLU;
    GeoLayer::point cornerRB;
    cornerLU.x = 13.236774;
    cornerRB.x = cornerLU.x + 325 * xInc;
    cornerRB.y = 48.802824;
    cornerLU.y = cornerRB.y + 170 * yInc;
    if (lat < cornerRB.x && lat > cornerLU.x)
    {
        if (lon > cornerRB.y && lon < cornerLU.y)
        {
            //calculate pixel position
            GeoLayer::point pixPos;
            pixPos.x = ((lat - cornerLU.x) / xInc);
            pixPos.y = ((cornerLU.y - lon) / yInc);
            //qDebug() << "Getting info for pixel" << pixPos.x << " " << pixPos.y;
            *temp = (int)tempGrid[(int)pixPos.y][(int)pixPos.x];
            if (*temp > 50 || *temp < 0)
                *temp = 0;
            int cloud = (int)cloudGrid[(int)pixPos.y][(int)pixPos.x];
            if (cloud < 0 || cloud > 100)
                cloud = 0;
            int rain = (int)rainGrid[(int)pixPos.y][(int)pixPos.x];
            //qDebug() << "Temp:" << *temp << "Clouds:" << cloud << "Rain:" << rain;
            if (rain < 0)
                rain = 0;
            if (cloud >= 50 && rain > 0)
                return "clouds_rain";
            if (cloud < 50 && rain > 0)
                return "clouds_sun_rain";
            if (cloud >= 70)
                return "clouds";
            if (cloud < 70 && cloud >= 30)
                return "clouds_sun";
            return "sun";
        }
    }
    return "sun";
}

void MapWindow::placeIcon(float x, float y)
{
    if (y > 1 || x > 1)
    {
        qDebug() << "Wrong x or y, should be below 1";
        return;
    }
    QPoint destPos = QPoint(ui->label->geometry().width() * x, ui->label->geometry().height() * y);

    int temp = 0;
    GeoLayer::point latLon = vPort->getLatLon(destPos);
    QString iconName = getIcon(latLon.x, latLon.y, &temp);
    //qDebug() << "Name:" << iconName << "Temp:" << temp;

    QString dir = QString("%1/icons/%2.png").arg(QDir::currentPath(), iconName);
    //qDebug() << "Dir:" << dir;
    QImage iconImg = QImage(dir);
    destPos = QPoint(ui->label->geometry().width() * x -32, ui->label->geometry().height() * y -32);
    QPainter painter(&imgCopy);
    //qDebug() << "Pointer ok";
    painter.drawImage(destPos, iconImg);
    if (temp < 10)
    {
        destPos.setY(destPos.y() + 46);
        painter.drawImage(destPos, numberImg[temp]);
        destPos.setX(destPos.x() + 10);
        painter.drawImage(destPos, numberImg[10]);
        destPos.setX(destPos.x() + 10);
        painter.drawImage(destPos, numberImg[11]);
    }
    else
    {
        destPos.setY(destPos.y() + 46);
        painter.drawImage(destPos, numberImg[temp/10]);
        destPos.setX(destPos.x() + 10);
        painter.drawImage(destPos, numberImg[temp%10]);
        destPos.setX(destPos.x() + 10);
        painter.drawImage(destPos, numberImg[10]);
        destPos.setX(destPos.x() + 10);
        painter.drawImage(destPos, numberImg[11]);
    }
    painter.end();
}

void MapWindow::drawIcons()
{
    for (int i = 1; i < 5; i++)
        placeIcon(0.2f * (float)i, 0.2f * (float)i);
    placeIcon(0.2f, 0.6f);
    placeIcon(0.4f, 0.8f);
    placeIcon(0.6f, 0.2f);
    placeIcon(0.8f, 0.4f);
    ui->label->setPixmap(QPixmap::fromImage(imgCopy));
    ui->label->show();
}

void MapWindow::updateGradient(float min, float max, QString text, QColor colorMin, QColor colorMax)
{
    ui->labelParam->setText(text);
    ui->labelMin->setText(QString::number(min));
    ui->labelMax->setText(QString::number(max));
    QImage image = QImage(150, 20, QImage::Format_RGB32);
    for (int i = 0; i < 150; i++)
    {
        float opacity = (float)i/150;
        QColor colorFinal = QColor(
                    (colorMax.red() * opacity) + (colorMin.red() * (1-opacity)),
                    (colorMax.green() * opacity) + (colorMin.green() * (1-opacity)),
                    (colorMax.blue() * opacity) + (colorMin.blue() * (1-opacity)),
                    255
                    );
        for (int j = 0; j < 20; j++)
        {
            image.setPixel(i, j, colorFinal.rgb());
        }
    }
    ui->gradientLabel->setPixmap(QPixmap::fromImage(image));
    ui->label->show();
}

clickableLabel * MapWindow::getLabel()
{
    return ui->label;
}

void MapWindow::resizeMap(int w, int h)
{
    ui->label->resize(w-40, h-40);
    vPort->resize(w-40, h-40);
    ui->legendGroup->setGeometry(w-450, h-25, 450, 25);
    emit resizeSignal();
}
