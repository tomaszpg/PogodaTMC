#include "clickablelabel.h"
#include <QDebug>
#include <QtEvents>

clickableLabel::clickableLabel( const QString & text, QWidget * parent )
:QLabel(parent)
{
    //connect( this, SIGNAL( clicked() ), this, SLOT( slotClicked() ) );
}

clickableLabel::clickableLabel( QWidget * parent )
:QLabel(parent)
{
    //connect( this, SIGNAL( clicked() ), this, SLOT( slotClicked() ) );
}

void clickableLabel::slotClicked()
{
    //qDebug()<<"Clicked";
}

void clickableLabel::mousePressEvent (QMouseEvent *event)
{
    position = event->pos();
    emit clicked();
}

QPoint clickableLabel::getPos()
{
    return position;
}
