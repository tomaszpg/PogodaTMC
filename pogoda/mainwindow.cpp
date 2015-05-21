#define _USE_MATH_DEFINES
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QString>
#include <QFile>
#include <QColor>
#include <QColorDialog>
#include <QTreeWidgetItem>
#include <QDebug>
#include <QMouseEvent>
#include <math.h>
#include <viewport.h>
#include <vector>
#include <QFileDialog>
#include <QDir>
#include "mapwindow.h"
#define deg2rad(d) (((d)*M_PI)/180)
#define rad2deg(d) (((d)*180)/M_PI)
#define earth_radius 6378137

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    setupGUI();
    setColors();
    wMetaData = new double[6];
    dlWMetaData();
    //vPort = new Viewport(512, 512, this);
    advancedMode = false;
    logPrint("Hello!");
    map = new MapWindow;
    map->show();
    vPort = map->getHandle();
    connect(map->getLabel(), SIGNAL (clicked()), this, SLOT (showPosition()));
    connect(map, SIGNAL (resizeSignal()), this, SLOT (refreshView()));
    layerNum=0;
    layers=new QVector<GeoLayer*>();
    //double dtest1 = lat2y_d(48.5);
    //double dtest2 = lat2y_d(55.4148);
    //qDebug() << dtest1 << dtest2;

}

double MainWindow::lat2y_d(double lat)
{
    return rad2deg(log(tan(M_PI/4+ deg2rad(lat)/2)));
}

double MainWindow::y2lat_d(double y)
{
    return rad2deg(2 * atan(exp(  deg2rad(y) ) ) - M_PI/2);
}

void MainWindow::setColors()
{
    colorMin = QColor(0, 255, 0, 255);
    if(colorMin.isValid())
    {
        QString qss = QString("background-color: %1").arg(colorMin.name());
        ui->bColor1->setStyleSheet(qss);
    }
    colorMax = QColor(255, 0, 0, 255);
    if(colorMax.isValid())
    {
        QString qss2 = QString("background-color: %1").arg(colorMax.name());
        ui->bColor2->setStyleSheet(qss2);
    }
}

void MainWindow::showPosition()
{
    QPoint point = map->getLabel()->getPos();
    GeoLayer::point latLonPoint = vPort->getLatLon(point);
    logPrint(QString("Szerokość: %1 Długość: %2").arg(QString::number (latLonPoint.x, 'g', 10), QString::number (latLonPoint.y, 'g', 10)));
    //qDebug() << point.x() << point.y();
}

void MainWindow::setupGUI()
{
    // dodanie listy wyboru godzin
    QStringList list;
    for (int i=0; i<24; i++)
    {
        list.append(QString::number(i));
    }
    ui->comboHour->addItems(list);
    list.clear();

    //dodanie listy wyboru paremetrów pogody
    ui->comboParam->addItem(QStringLiteral("Temperatura powietrza"), QStringLiteral("T2MEAN2m.csv"));
    ui->comboParam->addItem(QStringLiteral("Opady"), QStringLiteral("ACM_TOTAL_PERCIP.csv"));
    ui->comboParam->addItem(QStringLiteral("Niskie chmury"), QStringLiteral("LOW_CLOUD_FRACTION.csv"));
    ui->comboParam->addItem(QStringLiteral("Średnie chmury"), QStringLiteral("MID_CLOUD_FRACTION.csv"));
    ui->comboParam->addItem(QStringLiteral("Wysokie chmury"), QStringLiteral("HIGH_CLOUD_FRACTION.csv"));
    ui->comboParam->addItem(QStringLiteral("Wilgotność"), QStringLiteral("SURFACE_REL_HUMID.csv"));
}

MainWindow::~MainWindow()
{
    delete ui;
}

// przejscie do trybu zaawansowanego
void MainWindow::on_checkBox_clicked(bool checked)
{
    if (checked)
    {
        ui->groupAdvanced->setEnabled(true);
        ui->groupGraph->setEnabled(true);
        advancedMode = true;

    }
    else
    {
        ui->groupAdvanced->setEnabled(false);
        ui->groupGraph->setEnabled(false);
        advancedMode = false;
    }
}

// uruchomienie filtracji parametru
void MainWindow::on_checkFilter_clicked(bool checked)
{
    if (checked)
        ui->groupFilter->setEnabled(true);
    else
        ui->groupFilter->setEnabled(false);
}

// nalozenie obrazu parametrow na mape
void MainWindow::on_bShowWeather_clicked()
{
    QString fileUrl = QString("http://ksgmet.eti.pg.gda.pl/prognozy/CSV/poland/%1/%2/%3/%4/%5").arg(
                QString::number(ui->calendarWidget->selectedDate().year()),
                QString::number(ui->calendarWidget->selectedDate().month()),
                QString::number(ui->calendarWidget->selectedDate().day()),
                ui->comboHour->currentText(),
                (ui->comboParam->itemData(ui->comboParam->currentIndex())).toString()
                );
    //QUrl fileUrl("http://ksgmet.eti.pg.gda.pl/prognozy/CSV/poland/2015/4/11/11/ACM_CONVECTIVE_PERCIP.csv");
    m_pFileCtrl = new FileDownloader(QUrl(fileUrl), this);

    connect(m_pFileCtrl, SIGNAL (downloaded()), this, SLOT (processFile()));
}

void MainWindow::dlWMetaData()
{
    QString fileUrl = QString("http://ksgmet.eti.pg.gda.pl/prognozy/CSV/poland/%1/current.nfo").arg(
                QString::number(ui->calendarWidget->selectedDate().year())
                );
   n_pFileCtrl = new FileDownloader(QUrl(fileUrl), this);
   connect(n_pFileCtrl, SIGNAL (downloaded()), this, SLOT (setWMetaData()));
}

void MainWindow::setWMetaData()
{
    if (!n_pFileCtrl->downloadedData().isNull())
    {
        // PRZETWARZANIE PLIKU NFO (META)
        //ui->labelLog->setText("Plik wczytany.");
        QString data = (n_pFileCtrl->downloadedData());
        QRegExp rx("(\\ |\\,|\\t|\\n)");
        QStringList query = data.split(rx);
        wSizeX = query[7].toInt();
        wSizeY = query[8].toInt();
        wMetaData[0] = query[3].toDouble();
        wMetaData[1] = query[4].toDouble();
        wMetaData[2] = 0.0f;
        wMetaData[3] = (query[5].toDouble())+(query[6].toDouble()*(double)wSizeY);
        wMetaData[4] = 0.0f;
        wMetaData[5] = (query[6].toDouble());
        for (int i = 0; i < 6; i++)
        {
            ui->textBrowser->append(QString::number(wMetaData[i], 'g', 16));
        }
        ui->textBrowser->append(QString::number(wSizeX));
        ui->textBrowser->append(QString::number(wSizeY));
        ui->textBrowser->append(QString::number(wMetaData[1]/wMetaData[5]));
    }
}

void MainWindow::logPrint(QString text)
{
    ui->labelLog->setText(text);
}

void MainWindow::processFile()
{
    if (!m_pFileCtrl->downloadedData().isNull())
    {
        // PRZETWARZANIE PLIKU CSV
        ui->labelLog->setText("Plik wczytany.");
        QString data = (m_pFileCtrl->downloadedData());
        QRegExp rx("(\\ |\\,|\\t|\\n)");
        QStringList query = data.split(rx);
        query.removeAll(NULL);
        //logPrint(QString::number(query.size()));
        //logPrint(QString::number(query[325].toInt()));
        /*
        QStringList query;
        for (int i = 0; i < preQuery.size(); i++)
        {
            if (preQuery[i] != NULL)
                query.append(preQuery[i]);
        }
        */
        if (query.size() == 55250)
        {
            float** dataGrid = new float*[wSizeY];
            for(int i = 0; i < wSizeY; ++i)
                dataGrid[i] = new float[wSizeX];

            float maxValue = 0;
            float minValue = 9999.9f;
            float range = 0;

            //QRegExp re("\\d*");
            for (int i = 0; i < wSizeY; i++)
            {
                for (int j = 0; j < wSizeX; j++)
                {
                    dataGrid[i][j] = query[(wSizeY-i-1)*wSizeX + j].toFloat();
                    if (dataGrid[i][j] > maxValue)
                        maxValue = dataGrid[i][j];
                    if (dataGrid[i][j] > -9999.9f && dataGrid[i][j] < minValue)
                        minValue = dataGrid[i][j];
                }
            }

            range = maxValue - minValue;


            QRgb colorValue;
            QImage wLayer = QImage(325, 170, QImage::Format_RGB32);
            wLayer.fill(QColor(255,255,255,255));
            for (int i = 0; i < wSizeY; i++)
            {
                for (int j = 0; j < wSizeX; j++)
                {
                    float grad;
                    if (range != 0)
                        grad = (dataGrid[i][j] - minValue)/range;
                    else
                        grad = 0;

                    int redVal = colorMin.red()*(1-grad) + colorMax.red()*grad;
                    int greenVal = colorMin.green()*(1-grad) + colorMax.green()*grad;
                    int blueVal = colorMin.blue()*(1-grad) + colorMax.blue()*grad;
                    colorValue = qRgb(redVal, greenVal, blueVal);

                    if (dataGrid[i][j] > -9999.9f)
                        wLayer.setPixel(j, i, colorValue);
                }
            }
            GeoLayer::point cornerLU;
            GeoLayer::point cornerRB;
            cornerLU.x = wMetaData[0];
            cornerLU.y = wMetaData[3];
            cornerRB.x = wMetaData[0] + wSizeX * wMetaData[1];
            cornerRB.y = wMetaData[3] - wSizeY * wMetaData[5];
            GeoLayer*warstwa = new GeoLayer(&wLayer, 1, cornerLU, cornerRB, this);
            layers->append(warstwa);
            layerNum++;
            QTreeWidgetItem*item=new QTreeWidgetItem();
            QString tekst=QString("Warstwa")+QString::number((double)layerNum)+QString(" p");
            item->setText(0,tekst);
            item->setTextColor(0,QColor("red"));
            ui->treeWidget->addTopLevelItem(item);
            item->setData(0,Qt::UserRole,QVariant::fromValue<GeoLayer*>(warstwa));
            //QColor testColor = weatherLayer->getPixel(13.406774, 48.962824);
            //logPrint(QString::number(testColor.blue()));
            //wLayer = weatherLayer->getImage().copy();
            refreshView();
            /*
            wLayer = vPort->draw(weatherLayer, 255);
            //wLayer = wLayer.scaled(512, 512, Qt::IgnoreAspectRatio, Qt::SmoothTransformation);
            //qDebug() << wLayer.height() << wLayer.width();
            ui->imageLabel->setPixmap(QPixmap::fromImage(wLayer));
            ui->imageLabel->show();
            //ui->textBrowser->append(data);
            */

        }
        else
            logPrint(QString::number(query.size()));
    }
    else
    {
        ui->labelLog->setText("Brak pliku na serwerze.");
    }
}

void MainWindow::refreshView()
{
    vPort->clear();
    QImage image;
    if(layerNum>0)
    {
        for(int i=0;i<layerNum;i++)
        {
            GeoLayer*war=ui->treeWidget->topLevelItem(i)->data(0,Qt::UserRole).value<GeoLayer*>();
            if(war->visibility==true)
            {
                image = vPort->draw(war,128);
            }
        }
    }
    /*else
        image.fill(Qt::black);*/
    //ui->imageLabel->setPixmap(QPixmap::fromImage(image));
    //ui->imageLabel->show();
    map->drawImage(image);
}

void MainWindow::on_bColor1_clicked()
{
    QColor col = QColorDialog::getColor(colorMin, this);
    if(col.isValid())
    {
        colorMin = col;
        QString qss = QString("background-color: %1").arg(col.name());
        ui->bColor1->setStyleSheet(qss);
    }
}

void MainWindow::on_bColor2_clicked()
{
    QColor col = QColorDialog::getColor(colorMax, this);
    if(col.isValid())
    {
        colorMax = col;
        QString qss = QString("background-color: %1").arg(col.name());
        ui->bColor2->setStyleSheet(qss);
    }
}

void MainWindow::on_bNavUp_2_clicked()
{
    vPort->scaleDown();
    refreshView();
}

void MainWindow::on_bNavUp_3_clicked()
{
    vPort->scaleUp();
    refreshView();
}

void MainWindow::on_bNavUp_clicked()
{
    vPort->moveUp();
    refreshView();
}

void MainWindow::on_bNavDown_clicked()
{
    vPort->moveDown();
    refreshView();
}

void MainWindow::on_bNavRight_clicked()
{
    vPort->moveRight();
    refreshView();
}

void MainWindow::on_bNavLeft_clicked()
{
    vPort->moveLeft();
    refreshView();
}

void MainWindow::on_bLayerNew_clicked()
{
    QString fileName = QFileDialog::getOpenFileName(this,"Open Image File",QDir::currentPath());
    if(!fileName.isEmpty())
    {
        QImage Image = QImage(fileName,"PNM");
        GeoLayer::point corLU, corRB;
        corLU.x=19.45 - 5.625;
        corLU.y=y2lat_d(lat2y_d(48.5) + 11.25);
        corRB.x=19.45 + 5.625;
        corRB.y=48.5;
        GeoLayer*warstwa=new GeoLayer(&Image,1,corLU,corRB,this);
        layers->append(warstwa);
        layerNum++;
        QTreeWidgetItem*item=new QTreeWidgetItem();
        QString tekst=QString("Warstwa")+QString::number((double)layerNum);
        item->setText(0,tekst);
        item->setTextColor(0,QColor("red"));
        ui->treeWidget->addTopLevelItem(item);
        item->setData(0,Qt::UserRole,QVariant::fromValue<GeoLayer*>(warstwa));
    }
    refreshView();
}

void MainWindow::on_bLayerDelete_clicked()
{
    //ui->label_3->setText(QString(ui->treeWidget->currentItem()->text(0)));
    QTreeWidgetItem* item = ui->treeWidget->currentItem();
    int i = ui->treeWidget->indexOfTopLevelItem(item);
    ui->treeWidget->takeTopLevelItem(i);
    delete item;
    layerNum--;
    refreshView();
}

void MainWindow::on_bLayerUp_clicked()
{
    QTreeWidgetItem* item_down = ui->treeWidget->currentItem();
    QTreeWidgetItem* item_clone=item_down->clone();
    int index=ui->treeWidget->currentIndex().row();
    delete item_down;
    ui->treeWidget->insertTopLevelItem(index-1,item_clone);
    ui->treeWidget->setCurrentItem(item_clone);
    refreshView();
}

void MainWindow::on_bLayerDown_clicked()
{
    QTreeWidgetItem* item_down = ui->treeWidget->currentItem();
    QTreeWidgetItem* item_clone=item_down->clone();
    int index=ui->treeWidget->currentIndex().row();
    delete item_down;
    ui->treeWidget->insertTopLevelItem(index+1,item_clone);
    ui->treeWidget->setCurrentItem(item_clone);
    refreshView();
}

void MainWindow::on_treeWidget_itemClicked(QTreeWidgetItem *item, int column)
{

}

void MainWindow::on_bLayerVisibility_clicked()
{
    bool visible=ui->treeWidget->currentItem()->data(0,Qt::UserRole).value<GeoLayer*>()->visibility;
    ui->treeWidget->currentItem()->data(0,Qt::UserRole).value<GeoLayer*>()->visibility=!visible;
    if(!visible==true)
        ui->treeWidget->currentItem()->setTextColor(0,QColor("green"));
    else
        ui->treeWidget->currentItem()->setTextColor(0,QColor("red"));
    refreshView();
}
