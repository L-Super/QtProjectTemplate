#include <QApplication>
#include <QDebug>

#include "version.h"

int main(int argc, char* argv[])
{
	QApplication a(argc, argv);

	qDebug()<<QString("The version of this application is v%1").arg(VERSION_STR);
	return QApplication::exec();
}
