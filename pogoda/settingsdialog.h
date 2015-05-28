#ifndef SETTINGSDIALOG_H
#define SETTINGSDIALOG_H

#include <QDialog>
#include <QString>

namespace Ui {
class SettingsDialog;
}

class SettingsDialog : public QDialog
{
    Q_OBJECT

public:
    explicit SettingsDialog(QWidget *parent = 0);
    ~SettingsDialog();

private:
    Ui::SettingsDialog *ui;
    QString urlCoreString;
    QString folderStructString;
    QString metaDataString;

private slots:
    void setDefaultValues();
    void updateExample();
    void on_paramList_currentIndexChanged(const QString &arg1);
    void on_b_editRecord_clicked();
    void on_b_addRecord_clicked();
    void on_b_deleteRecord_clicked();
    void on_b_save_2_clicked();
    void on_folderStr_textChanged(const QString &arg1);
    void on_urlCore_textChanged(const QString &arg1);
    void on_metaUrl_textChanged(const QString &arg1);

    void on_buttonBox_accepted();

public slots:
    QString getMetaUrl();
    int getParamNumber();
    void getParamList(QString *str1, QString *str2, int index);
    QString getUrl();

signals:
    void settingsChanged();
};

#endif // SETTINGSDIALOG_H
