#ifndef FILEDOWNLOADER_H
#define FILEDOWNLOADER_H

#include <QObject>
#include <QByteArray>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>

class FileDownloader : public QObject
{
 Q_OBJECT
 public:
  explicit FileDownloader(QUrl fileUrl, int number=0, QObject *parent = 0);
  virtual ~FileDownloader();
  QByteArray downloadedData() const;

 signals:
  void downloaded(int num);

 private slots:
  void fileDownloaded(QNetworkReply* pReply);

 private:
  QNetworkAccessManager m_WebCtrl;
  QByteArray m_DownloadedData;
  int num;
};

#endif // FILEDOWNLOADER_H
