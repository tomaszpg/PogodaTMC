#ifndef CLICKABLELABEL
#define CLICKABLELABEL

#include <QLabel>
#include <QPoint>

class clickableLabel : public QLabel
{
    Q_OBJECT
public:
    clickableLabel(const QString & text, QWidget * parent = 0);
    clickableLabel(QWidget * parent = 0 );
    ~clickableLabel(){}
    QPoint position;
    QPoint getPos();

signals:
    void clicked();

public slots:
    void slotClicked();

protected:
    void mousePressEvent (QMouseEvent * event) ;

};

#endif // CLICKABLELABEL

