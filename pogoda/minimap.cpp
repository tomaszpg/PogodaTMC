#include "minimap.h"
#include "ui_minimap.h"
#include <QDir>
#include <QFileInfo>
#include <QDebug>

bool fileExists(QString path) {
    QFileInfo checkFile(path);
    // check if file exists and if yes: Is it really a file and no directory?
    if (checkFile.exists() && checkFile.isFile()) {
        return true;
    } else {
        return false;
    }
}

MiniMap::MiniMap(Viewport *vPortPoiner, QWidget *parent) :
    QDialog(parent),
    ui(new Ui::MiniMap)
{
    ui->setupUi(this);
    QString path = QDir::currentPath() + "/minimap.png";
    if (fileExists(path))
    {
       image = new QImage(path);
       ui->labelMap->setPixmap(QPixmap::fromImage(*image));
       ui->labelMap->show();
    }
    else
    {
        qDebug() << "Plik " << path << " nie istnieje.";
    }
    connect(ui->labelMap, SIGNAL (clicked()), this, SLOT (goToPos()));
    vPort = &*vPortPoiner;
}

void MiniMap::goToPos()
{
    vPort->goToMinimapPos(ui->labelMap->getPos().x(), ui->labelMap->getPos().y());
    getBox();
}

void MiniMap::getBox()
{
    int a, b, c, d;
    vPort->getBoundingBox(&a, &b, &c, &d);
    drawBox(a, b, c, d);
}

void MiniMap::drawBox(int leftUpperX, int leftUpperY, int rightBottomX, int rightBottomY)
{
    QImage newImage;
    newImage = QImage(*image);
    for (int i = leftUpperX; i < rightBottomX; i++)
    {
        newImage.setPixel(i, leftUpperY, Qt::red);
        newImage.setPixel(i, rightBottomY, Qt::red);
    }
    for (int i = leftUpperY; i < rightBottomY; i++)
    {
        newImage.setPixel(leftUpperX, i, Qt::green);
        newImage.setPixel(rightBottomX, i, Qt::green);
    }
    ui->labelMap->setPixmap(QPixmap::fromImage(newImage));
    ui->labelMap->show();
}

MiniMap::~MiniMap()
{
    delete ui;
}
