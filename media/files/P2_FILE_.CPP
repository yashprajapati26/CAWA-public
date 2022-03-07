#include<iostream.h>
#include<conio.h>
#include<fstream.h>
void main()
{
clrscr();
	ofstream outf("p1_fileIO.txt");

	cout<<"Enter student name:";
	char name[20];
	cin>>name;

	outf<<"Stu name :"<<name<<"\n";

	cout<<"Enter Roll No:";
	int no;
	cin>>no;

	outf<<"Roll no :"<<no<<"\n";

	outf.close();

	ifstream outp("p1_fileIO.txt");
	outp>>name;
	outp>>no;
	cout<<name<<"\t"<<no;
	outp.close();


getch();
}