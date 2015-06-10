#include "filedownloader.h"

FileDownloader::FileDownloader(QUrl fileUrl,int number, QObject *parent) :
 QObject(parent)
{
  num=number;
 connect(
  &m_WebCtrl, SIGNAL (finished(QNetworkReply*)),
  this, SLOT (fileDownloaded(QNetworkReply*))
  );

 QNetworkRequest request(fileUrl);
 m_WebCtrl.get(request);
}

FileDownloader::~FileDownloader() { }

void FileDownloader::fileDownloaded(QNetworkReply* pReply) {
 m_DownloadedData = pReply->readAll();
 //emit a signal
 pReply->deleteLater();
 emit downloaded(num);
}

QByteArray FileDownloader::downloadedData() const {
 return m_DownloadedData;
}
