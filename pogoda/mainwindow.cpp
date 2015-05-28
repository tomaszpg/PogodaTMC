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
//#include "gdal_priv.h"
//#include "cpl_conv.h"
#define deg2rad(d) (((d)*M_PI)/180)
#define rad2deg(d) (((d)*180)/M_PI)
#define earth_radius 6378137

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    settings = new SettingsDialog;
    setupGUI();
    setColors();
    wMetaData = new double[6];
    //vPort = new Viewport(512, 512, this);
    advancedMode = true;
    logPrint("Hello! New");
    map = new MapWindow;
    map->show();
    miniMap = new MiniMap(map->getHandle(), this);
    miniMap->show();
    vPort = map->getHandle();
    dlWMetaData();
    connect(map->getLabel(), SIGNAL (clicked()), this, SLOT (showPosition()));
    connect(map, SIGNAL (resizeSignal()), this, SLOT (refreshView()));
    connect(vPort, SIGNAL (refresh()), this, SLOT (refreshView()));
    connect(settings, SIGNAL (settingsChanged()), this, SLOT (updateSettings()));
    layerNum=0;
    layers=new QVector<GeoLayer*>();
    layerNum_osm=0;
    layers_osm=new QVector<GeoLayer*>();
    zoom=7.0;
    flaga=false;
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

void MainWindow::updateSettings()
{
    ui->comboParam->clear();
    int num = settings->getParamNumber();
    for (int i = 0; i < num; i++)
    {
        QString str1, str2;
        settings->getParamList(&str1, &str2, i);
        ui->comboParam->addItem(str1, str2);
    }
}

QString MainWindow::parseUrl(QString url)
{
    QRegExp rx("(\\%)");
    QStringList query = url.split(rx);
    for (int i = 0; i < query.length(); i++)
    {
        if (!QString::compare(query[i], "y/", Qt::CaseSensitive))
            query[i] = QString("%1/").arg(QString::number(ui->calendarWidget->selectedDate().year()));
        if (!QString::compare(query[i], "m/", Qt::CaseSensitive))
            query[i] = QString("%1/").arg(QString::number(ui->calendarWidget->selectedDate().month()));
        if (!QString::compare(query[i], "d/", Qt::CaseSensitive))
            query[i] = QString("%1/").arg(QString::number(ui->calendarWidget->selectedDate().day()));
        if (!QString::compare(query[i], "h/", Qt::CaseSensitive))
            query[i] = QString("%1/").arg(ui->comboHour->currentText());
    }
    url = QString();
    for (int i = 0; i < query.length(); i++)
    {
        url.append(query[i]);
    }
    url.append((ui->comboParam->itemData(ui->comboParam->currentIndex())).toString());
    qDebug() << url;
    return url;
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

    updateSettings();
    //dodanie listy wyboru paremetrów pogody
    /*
    ui->comboParam->addItem(QStringLiteral("Temperatura powietrza [K]"), QStringLiteral("T2MEAN2m.csv"));
    ui->comboParam->addItem(QStringLiteral("Opady [mm H2O]"), QStringLiteral("ACM_TOTAL_PERCIP.csv"));
    ui->comboParam->addItem(QStringLiteral("Niskie chmury [%]"), QStringLiteral("LOW_CLOUD_FRACTION.csv"));
    ui->comboParam->addItem(QStringLiteral("Średnie chmury [%]"), QStringLiteral("MID_CLOUD_FRACTION.csv"));
    ui->comboParam->addItem(QStringLiteral("Wysokie chmury [%]"), QStringLiteral("HIGH_CLOUD_FRACTION.csv"));
    ui->comboParam->addItem(QStringLiteral("Wilgotność [%]"), QStringLiteral("SURFACE_REL_HUMID.csv"));
    */
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
    /*
    QString fileUrl = QString("http://ksgmet.eti.pg.gda.pl/prognozy/CSV/poland/%1/%2/%3/%4/%5").arg(
                QString::number(ui->calendarWidget->selectedDate().year()),
                QString::number(ui->calendarWidget->selectedDate().month()),
                QString::number(ui->calendarWidget->selectedDate().day()),
                ui->comboHour->currentText(),
                (ui->comboParam->itemData(ui->comboParam->currentIndex())).toString()
                );
    */
    QString fileUrl = parseUrl(settings->getUrl());
    //QUrl fileUrl("http://ksgmet.eti.pg.gda.pl/prognozy/CSV/poland/2015/4/11/11/ACM_CONVECTIVE_PERCIP.csv");
    m_pFileCtrl = new FileDownloader(QUrl(fileUrl), this);

    connect(m_pFileCtrl, SIGNAL (downloaded()), this, SLOT (processFile()));
}

void MainWindow::dlWMetaData()
{
    /*
    QString fileUrl = QString("http://ksgmet.eti.pg.gda.pl/prognozy/CSV/poland/%1/current.nfo").arg(
                QString::number(ui->calendarWidget->selectedDate().year())
                );
                */
   QString fileUrl = settings->getMetaUrl();
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
            //ui->textBrowser->append(QString::number(wMetaData[i], 'g', 16));
        }
        //ui->textBrowser->append(QString::number(wSizeX));
        //ui->textBrowser->append(QString::number(wSizeY));
        //ui->textBrowser->append(QString::number(wMetaData[1]/wMetaData[5]));
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
            map->updateGradient(minValue, maxValue, ui->comboParam->currentText(), colorMin, colorMax);
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
    if(ui->tabMapType->currentIndex()==0)
    {
        if(layerNum>0)
        {
            for(int i=0;i<layerNum;i++)
            {
                GeoLayer*war=ui->treeWidget->topLevelItem(i)->data(0,Qt::UserRole).value<GeoLayer*>();
                if(i==0)
                {
                    vPort->setCorners(war->cornerLU,war->cornerRB);
                }
                if(war->visibility==true)
                {
                    image = vPort->draw(war,128);
                }
            }
        }
    }
    else if(ui->tabMapType->currentIndex()==1)
    {
        if(layerNum_osm>0)
        {
            for(int i=0;i<layerNum_osm;i++)
            {
                GeoLayer*war=ui->treeWidget_2->topLevelItem(i)->data(0,Qt::UserRole).value<GeoLayer*>();
                if(i==0)
                {
                    vPort->setCorners(war->cornerLU,war->cornerRB);
                }
                if(war->visibility==true)
                {
                    image = vPort->draw(war,128);
                }
            }
        }
    }
    /*else
        image.fill(Qt::black);*/
    //ui->imageLabel->setPixmap(QPixmap::fromImage(image));
    //ui->imageLabel->show();
    map->drawImage(image);
    miniMap->getBox();
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
    if(ui->tabMapType->currentIndex()==0)
        vPort->scaleDown();
    else if(layerNum_osm>0)
    {
        double lon=ui->textEdit->toPlainText().toDouble();
        double lat=ui->textEdit_2->toPlainText().toDouble();
        zoom++;
        double n=pow(2.0,zoom);
        double x=deg2rad(lon);
        double y=asinh(tan(deg2rad(lat)));
        x=round(n*(1+(x/M_PI))/2);
        y=round(n*(1-(y/M_PI))/2);
        GeoLayer::point cornerLU, cornerRB;
        cornerLU.x=lon;
        cornerLU.y=lat;
        double dangle_lon=360.0/n;
        double dangle_lat=170.1022/n;
        cornerRB.x=cornerLU.x+dangle_lon;
        cornerRB.y=cornerLU.y-dangle_lat;
        int i=ui->treeWidget_2->currentIndex().row();
        GeoLayer*war=ui->treeWidget_2->topLevelItem(i)->data(0,Qt::UserRole).value<GeoLayer*>();
        war->setCorners(cornerLU, cornerRB);
        flaga=true;
        QString fileUrl = QString("http://otile1.mqcdn.com/tiles/1.0.0/osm/%1/%2/%3.jpg").arg(
                    QString::number(zoom),
                    QString::number(x),
                    QString::number(y)
                    );
        osm_pFileCtrl = new FileDownloader(QUrl(fileUrl), this);
        connect(osm_pFileCtrl, SIGNAL (downloaded()), this, SLOT (show_url_image()));
    }
    refreshView();
}

void MainWindow::on_bNavUp_3_clicked()
{
    if(ui->tabMapType->currentIndex()==0)
        vPort->scaleUp();
    else if(layerNum_osm>0)
    {
        double lon=ui->textEdit->toPlainText().toDouble();
        double lat=ui->textEdit_2->toPlainText().toDouble();
        zoom--;
        double n=pow(2.0,zoom);
        double x=deg2rad(lon);
        double y=asinh(tan(deg2rad(lat)));
        x=round(n*(1+(x/M_PI))/2);
        y=round(n*(1-(y/M_PI))/2);
        GeoLayer::point cornerLU, cornerRB;
        cornerLU.x=lon;
        cornerLU.y=lat;
        double dangle_lon=360.0/n;
        double dangle_lat=170.1022/n;
        cornerRB.x=cornerLU.x+dangle_lon;
        cornerRB.y=cornerLU.y-dangle_lat;
        int i=ui->treeWidget_2->currentIndex().row();
        GeoLayer*war=ui->treeWidget_2->topLevelItem(i)->data(0,Qt::UserRole).value<GeoLayer*>();
        war->setCorners(cornerLU, cornerRB);
        flaga=true;
        QString fileUrl = QString("http://otile1.mqcdn.com/tiles/1.0.0/osm/%1/%2/%3.jpg").arg(
                    QString::number(zoom),
                    QString::number(x),
                    QString::number(y)
                    );
        osm_pFileCtrl = new FileDownloader(QUrl(fileUrl), this);
        connect(osm_pFileCtrl, SIGNAL (downloaded()), this, SLOT (show_url_image()));
    }
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
    //GDALDataset *poDataset;
    //GDALAllRegister();
    QString fileName = QFileDialog::getOpenFileName(this,"Open Image File",QDir::currentPath());
    //QByteArray array =fileName.toLocal8Bit();
    //char* buffer = array.data();
    //poDataset = (GDALDataset *) GDALOpen( buffer, GA_ReadOnly );
    //ui->textBrowser->setText(QString::fromUtf8(poDataset->GetProjectionRef(),5));
    if(1)
    {
        //double*coefficients=new double[6];
        //poDataset->GetGeoTransform(coefficients);
        QImage Image = QImage(fileName,"PNM");
        GeoLayer::point corLU, corRB;
        corLU.x=19.45 - 5.625;
        corLU.y=y2lat_d(lat2y_d(48.5) + 11.25);
        corRB.x=19.45 + 5.625;
        corRB.y=48.5;
        //ui->label_3->setText(QString::number(corRB.x-corLU.x));
        //ui->label_4->setText(QString::number(corLU.y-corRB.y));
        ui->textEdit->setText(QString::number(corLU.x));
        ui->textEdit_2->setText(QString::number(corLU.y));
        GeoLayer*warstwa=new GeoLayer(&Image,1,corLU,corRB,this);
        layers->append(warstwa);
        layerNum++;
        //vPort->setCorners(corLU, corRB);
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
    layers->remove(i);
    layerNum--;
    refreshView();
}

void MainWindow::on_bLayerUp_clicked()
{
    if(ui->treeWidget->currentIndex().row()>0)
    {
        QTreeWidgetItem* item_down = ui->treeWidget->currentItem();
        QTreeWidgetItem* item_clone=item_down->clone();
        int index=ui->treeWidget->currentIndex().row();
        delete item_down;
        ui->treeWidget->insertTopLevelItem(index-1,item_clone);
        ui->treeWidget->setCurrentItem(item_clone);
        refreshView();
    }
}

void MainWindow::on_bLayerDown_clicked()
{
    if(ui->treeWidget->currentIndex().row()<layerNum-1)
    {
        QTreeWidgetItem* item_down = ui->treeWidget->currentItem();
        QTreeWidgetItem* item_clone=item_down->clone();
        int index=ui->treeWidget->currentIndex().row();
        delete item_down;
        ui->treeWidget->insertTopLevelItem(index+1,item_clone);
        ui->treeWidget->setCurrentItem(item_clone);
        refreshView();
    }
}

void MainWindow::on_treeWidget_itemClicked(QTreeWidgetItem *item, int column)
{

}

void MainWindow::on_bLayerVisibility_clicked()
{
    if(layerNum>0 && ui->treeWidget->currentIndex().row()>=0)
    {
        bool visible=ui->treeWidget->currentItem()->data(0,Qt::UserRole).value<GeoLayer*>()->visibility;
        ui->treeWidget->currentItem()->data(0,Qt::UserRole).value<GeoLayer*>()->visibility=!visible;
        if(!visible==true)
            ui->treeWidget->currentItem()->setTextColor(0,QColor("green"));
        else
            ui->treeWidget->currentItem()->setTextColor(0,QColor("red"));
        refreshView();
    }
}

void MainWindow::on_pushButton_clicked()
{
    double lon=ui->textEdit->toPlainText().toDouble();
    double lat=ui->textEdit_2->toPlainText().toDouble();
    double n=pow(2.0,zoom);
    double x=deg2rad(lon);
    double y=asinh(tan(deg2rad(lat)));
    x=round(n*(1+(x/M_PI))/2);
    y=round(n*(1-(y/M_PI))/2);
    //ui->label_3->setText(QString::number(x));
    //ui->label_4->setText(QString::number(y));
    QString fileUrl = QString("http://otile1.mqcdn.com/tiles/1.0.0/osm/%1/%2/%3.jpg").arg(
                QString::number(zoom),
                QString::number(x),
                QString::number(y)
                );
    osm_pFileCtrl = new FileDownloader(QUrl(fileUrl), this);
    connect(osm_pFileCtrl, SIGNAL (downloaded()), this, SLOT (show_url_image()));
}
void MainWindow::show_url_image()
{
    if (!osm_pFileCtrl->downloadedData().isNull())
    {
        if(flaga==false)
        {
            double lon=ui->textEdit->toPlainText().toDouble();
            double lat=ui->textEdit_2->toPlainText().toDouble();
            double n=pow(2.0,zoom);
            GeoLayer::point cornerLU, cornerRB;
            cornerLU.x=lon;
            cornerLU.y=lat;
            double dangle_lon=360.0/n;
            double dangle_lat=170.1022/n;
            cornerRB.x=cornerLU.x+dangle_lon;
            cornerRB.y=cornerLU.y-dangle_lat;
            QImage image;
            image.loadFromData(osm_pFileCtrl->downloadedData());
            GeoLayer*warstwa=new GeoLayer(&image,1,cornerLU,cornerRB,this);
            layers_osm->append(warstwa);
            layerNum_osm++;
            QTreeWidgetItem*item=new QTreeWidgetItem();
            QString tekst=QString("Warstwa")+QString::number((double)layerNum_osm)+QString("-OSM");
            item->setText(0,tekst);
            item->setTextColor(0,QColor("red"));
            ui->treeWidget_2->addTopLevelItem(item);
            item->setData(0,Qt::UserRole,QVariant::fromValue<GeoLayer*>(warstwa));
        }
        else
        {
            int i=ui->treeWidget_2->currentIndex().row();
            QImage image;
            image.loadFromData(osm_pFileCtrl->downloadedData());
            GeoLayer*war=ui->treeWidget_2->topLevelItem(i)->data(0,Qt::UserRole).value<GeoLayer*>();
            war->setImage(image);
            flaga=false;
            ui->treeWidget_2->currentItem()->setData(0,Qt::UserRole,QVariant::fromValue<GeoLayer*>(war));
        }
        refreshView();
    }
}

void MainWindow::on_actionUstawienia_programu_triggered()
{
    settings->show();
}

void MainWindow::on_bLayerVisibility_2_clicked()
{
    if(layerNum_osm>0 && ui->treeWidget_2->currentIndex().row()>=0)
    {
        bool visible=ui->treeWidget_2->currentItem()->data(0,Qt::UserRole).value<GeoLayer*>()->visibility;
        ui->treeWidget_2->currentItem()->data(0,Qt::UserRole).value<GeoLayer*>()->visibility=!visible;
        if(!visible==true)
            ui->treeWidget_2->currentItem()->setTextColor(0,QColor("green"));
        else
            ui->treeWidget_2->currentItem()->setTextColor(0,QColor("red"));
        refreshView();
    }
}

void MainWindow::on_bLayerUp_2_clicked()
{
    if(ui->treeWidget_2->currentIndex().row()>0)
    {
        QTreeWidgetItem* item_down = ui->treeWidget_2->currentItem();
        QTreeWidgetItem* item_clone=item_down->clone();
        int index=ui->treeWidget_2->currentIndex().row();
        delete item_down;
        ui->treeWidget_2->insertTopLevelItem(index-1,item_clone);
        ui->treeWidget_2->setCurrentItem(item_clone);
        refreshView();
    }
}

void MainWindow::on_bLayerDown_2_clicked()
{
    if(ui->treeWidget_2->currentIndex().row()<layerNum_osm-1)
    {
        QTreeWidgetItem* item_down = ui->treeWidget_2->currentItem();
        QTreeWidgetItem* item_clone=item_down->clone();
        int index=ui->treeWidget_2->currentIndex().row();
        delete item_down;
        ui->treeWidget_2->insertTopLevelItem(index+1,item_clone);
        ui->treeWidget_2->setCurrentItem(item_clone);
        refreshView();
    }
}

void MainWindow::on_tabMapType_currentChanged(int index)
{
    refreshView();
}

void MainWindow::on_bLayerDelete_2_clicked()
{
    QTreeWidgetItem* item = ui->treeWidget_2->currentItem();
    int i = ui->treeWidget_2->indexOfTopLevelItem(item);
    ui->treeWidget_2->takeTopLevelItem(i);
    delete item;
    layers_osm->remove(i);
    layerNum_osm--;
    refreshView();
}
