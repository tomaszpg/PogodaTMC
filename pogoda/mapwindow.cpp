#include "mapwindow.h"
#include "ui_mapwindow.h"


MapWindow::MapWindow(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::MapWindow)
{
    ui->setupUi(this);
    vPort = new Viewport(512, 512, this);
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
