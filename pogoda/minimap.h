#ifndef MINIMAP_H
#define MINIMAP_H

#include <QDialog>
#include <QImage>
#include "viewport.h"

namespace Ui {
class MiniMap;
}

class MiniMap : public QDialog
{
    Q_OBJECT

public:
    explicit MiniMap(Viewport *vPortPoiner, QWidget *parent = 0);
    ~MiniMap();

private:
    Ui::MiniMap *ui;
    QImage *image;
    Viewport *vPort;

private slots:
    void goToPos();
    void drawBox(int leftUpperX, int leftUpperY, int rightBottomX, int rightBottomY);

public slots:
    void getBox();
};

#endif // MINIMAP_H
