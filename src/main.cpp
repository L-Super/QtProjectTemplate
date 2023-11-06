#include <QApplication>
#include <QDebug>

int main(int argc, char* argv[])
{
	QApplication a(argc, argv);
	qDebug()<<"hello world";
	return QApplication::exec();
}
