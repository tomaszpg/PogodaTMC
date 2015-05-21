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

clickableLabel * MapWindow::getLabel()
{
    return ui->label;
}

void MapWindow::resizeMap(int w, int h)
{
    ui->label->resize(w, h);
    vPort->resize(w, h);
    emit resizeSignal();
}
