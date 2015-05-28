#include "settingsdialog.h"
#include "ui_settingsdialog.h"

SettingsDialog::SettingsDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::SettingsDialog)
{
    ui->setupUi(this);
    setDefaultValues();
}

SettingsDialog::~SettingsDialog()
{
    delete ui;
}

void SettingsDialog::setDefaultValues()
{
    urlCoreString = "http://ksgmet.eti.pg.gda.pl/prognozy/CSV/poland/";
    ui->urlCore->setText(urlCoreString);
    folderStructString = "%y/%m/%d/%h/";
    ui->folderStr->setText(folderStructString);
    updateExample();
    metaDataString = "http://ksgmet.eti.pg.gda.pl/prognozy/CSV/poland/2015/current.nfo";
    ui->metaUrl->setText(metaDataString);
    ui->paramList->clear();
    ui->paramList->addItem(QStringLiteral("Temperatura powietrza [K]"), QStringLiteral("T2MEAN2m.csv"));
    ui->paramList->addItem(QStringLiteral("Opady [mm H2O]"), QStringLiteral("ACM_TOTAL_PERCIP.csv"));
    ui->paramList->addItem(QStringLiteral("Niskie chmury [%]"), QStringLiteral("LOW_CLOUD_FRACTION.csv"));
    ui->paramList->addItem(QStringLiteral("Średnie chmury [%]"), QStringLiteral("MID_CLOUD_FRACTION.csv"));
    ui->paramList->addItem(QStringLiteral("Wysokie chmury [%]"), QStringLiteral("HIGH_CLOUD_FRACTION.csv"));
    ui->paramList->addItem(QStringLiteral("Wilgotność [%]"), QStringLiteral("SURFACE_REL_HUMID.csv"));
    ui->fileEdit->setText((ui->paramList->itemData(ui->paramList->currentIndex())).toString());
    ui->nameEdit->setText(ui->paramList->currentText());
}

void SettingsDialog::updateExample()
{
    QString newText = QString("URL: %1%2file.ext").arg(urlCoreString, folderStructString);
    ui->urlLabel->setText(newText);
}

QString SettingsDialog::getMetaUrl()
{
    return metaDataString;
}

QString SettingsDialog::getUrl()
{
    QString url = QString("%1%2").arg(urlCoreString, folderStructString);
    return url;
}

int SettingsDialog::getParamNumber()
{
    return ui->paramList->count();
}

void SettingsDialog::getParamList(QString *str1, QString *str2, int index)
{
    *str1 = ui->paramList->itemText(index);
    *str2 = ui->paramList->itemData(index).toString();
}

void SettingsDialog::on_paramList_currentIndexChanged(const QString &arg1)
{
    ui->fileEdit->setText((ui->paramList->itemData(ui->paramList->currentIndex())).toString());
    ui->nameEdit->setText(ui->paramList->currentText());
}

void SettingsDialog::on_b_editRecord_clicked()
{
    ui->paramList->setItemText(ui->paramList->currentIndex(), ui->nameEdit->text());
    ui->paramList->setItemData(ui->paramList->currentIndex(), ui->fileEdit->text());
}

void SettingsDialog::on_b_addRecord_clicked()
{
    ui->paramList->addItem(ui->nameNew->text(), ui->fileNew->text());
}

void SettingsDialog::on_b_deleteRecord_clicked()
{
    ui->paramList->removeItem(ui->paramList->currentIndex());
}

void SettingsDialog::on_b_save_2_clicked()
{
    setDefaultValues();
}

void SettingsDialog::on_folderStr_textChanged(const QString &arg1)
{
    folderStructString = ui->folderStr->text();
    updateExample();
}

void SettingsDialog::on_urlCore_textChanged(const QString &arg1)
{
    urlCoreString = ui->urlCore->text();
    updateExample();
}

void SettingsDialog::on_metaUrl_textChanged(const QString &arg1)
{
    metaDataString = ui->metaUrl->text();
}

void SettingsDialog::on_buttonBox_accepted()
{
    emit settingsChanged();
}
