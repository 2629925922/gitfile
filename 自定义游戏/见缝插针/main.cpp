/*********************************************************************
Use EGE (Easy Graphic Engeer, https://xege.org/ ) graphic library to
draw random lines on screen.

Need to add some parameters to compiling options. Please click menu
"Options > Compiler Options", in the textbox under "Add the following
commands when calling the linker:", do as following:
(a) if the current compiler set contains "64-bit", add:
  -lgraphics64 -luuid -lmsimg32 -lgdi32 -limm32 -lole32 -loleaut32
(b) if the current compiler set contains "32-bit", add:
  -lgraphics -luuid -lmsimg32 -lgdi32 -limm32 -lole32 -loleaut32

(These parameters are only for programs using EGE graphic library.
Please delete them for other programs which donot use EGE.)

˵������������ʹ���� EGE ͼ�κ����⣨https://xege.org/�����л�ͼ������ʱ
������Ļ�������������������ֱ���û��������������
��Ҫ�ڱ���ѡ���м���һЩ���Ӳ������ܳɹ����롣�������£����Dev-C++
�Ĳ˵������ߡ��еġ�����ѡ����ڡ����������������м�����������·���
�ı����У����ݱ����������ö�����������֣�ʵ������Ҫ��������ʱ�Ѷ��
�����������������ָ������Ϊͼ�ν��棩��
��A�������ǰʹ�õı��������а����С�64λ��������ӣ�
  -lgraphics64 -luuid -lmsimg32 -lgdi32 -limm32 -lole32 -loleaut32
��B�������ǰʹ�õı��������а����С�32λ��������ӣ�
  -lgraphics -luuid -lmsimg32 -lgdi32 -limm32 -lole32 -loleaut32
*********************************************************************/

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <graphics.h>	//EGE graphic library
#include <conio.h>
using namespace std;

int main() {
	const int width = 800, height = 600;
	int x1 = 0, y1 = height / 2, x2 = width / 6, y2 = height / 2;
	int linelength = width / 6;
	int score = 0;
	char s[20];
	itoa(score, s, 10);
	initgraph(width, height);
	setcolor(RED);
	setbkcolor(LIGHTGRAY);
	line(x1, y1, x2, y2);
	setfont(30, 0, "����");
	while (1) {
		outtextxy(width / 8, height / 6, "�÷�: ");
		outtextxy(width / 4, height / 6, s);
		circle(width / 2, height / 2, 60);
	}
	closegraph();
	return 0;
}
