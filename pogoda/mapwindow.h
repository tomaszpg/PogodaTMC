#ifndef MAPWINDOW_H
#define MAPWINDOW_H

#include <QDialog>
#include "viewport.h"
#include <QImage>
#include "clickablelabel.h"

namespace Ui {
class MapWindow;
}

class MapWindow : public QDialog
{
    Q_OBJECT

public:
    explicit MapWindow(QWidget *parent = 0);
    ~MapWindow();

private:
    Ui::MapWindow *ui;
    Viewport *vPort;
    QObject myParent;

public slots:
    Viewport * getHandle();
    void drawImage(QImage image);
    clickableLabel * getLabel();
    void updateGradient(float min, float max, QString text, QColor colorMin, QColor colorMax);

private slots:
    void resizeEvent(QResizeEvent *);
    void resizeMap(int w, int h);

signals:
    void resizeSignal();
};

#endif // MAPWINDOW_H
