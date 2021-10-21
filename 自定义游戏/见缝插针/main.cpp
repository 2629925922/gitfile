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
说明：本程序中使用了 EGE 图形函数库（https://xege.org/）进行绘图，运行时
会在屏幕上连续绘制随机线条，直到用户按任意键结束。
需要在编译选项中加入一些连接参数才能成功编译。操作如下：点击Dev-C++
的菜单“工具”中的“编译选项”，在“在连接器命令行中加入以下命令”下方的
文本框中，根据编译器的配置而添加如下文字（实际上是要求在连接时把多个
函数库包含进来，并指定程序为图形界面）：
（A）如果当前使用的编译配置中包含有“64位”，则添加：
  -lgraphics64 -luuid -lmsimg32 -lgdi32 -limm32 -lole32 -loleaut32
（B）如果当前使用的编译配置中包含有“32位”，则添加：
  -lgraphics -luuid -lmsimg32 -lgdi32 -limm32 -lole32 -loleaut32
*********************************************************************/

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <graphics.h>	//EGE graphic library
#include <conio.h>
#include <math.h>
using namespace std;

int main() {
	const int width = 1000, height = 600;
	const float pi = 3.1415926;
	int x1 = 0, y1 = height / 2, x2 = width / 6, y2 = height / 2;
	int linelength = width / 6;
	int score = 0;
	char s[20];
	float ratespeed = pi / 360;
	char input;
	int XEND, YEND;
	int sumspeed[1000];
	int numneedle = 0;
	initgraph(width, height);
	setcolor(BLACK);
	setbkcolor(WHITE);
	line(x1, y1, x2, y2);
	setlinestyle(SOLID_LINE, 3);
	setfont(30, 0, "宋体");
	setfillcolor(EGERGB(0X00, 0XFF, 0X00));
	while (1) {
		itoa(score, s, 10);
		outtextxy(width / 8, height / 6, "得分: ");
		outtextxy(width / 4, height / 6, s);
		fillellipse(width / 2, height / 2, width / 10, height / 6);
		for (int i = 0; i < numneedle; i++) {
			sumspeed[i] = sumspeed [i] + ratespeed;
			XEND = linelength * cos(-sumspeed[i]) + width / 2;
			YEND = linelength * sin(-sumspeed[i]) + height / 2;
			setcolor(BLUE);
			line(width / 2, height / 2, XEND, YEND);
		}
		if (!kbhit() && ratespeed != 0) {
			input = getch();
			if (input == ' ') {
				numneedle++;
				sumspeed[numneedle - 1] = pi;
				XEND = linelength * cos(-sumspeed[numneedle - 1]) + width / 2;
				YEND = linelength * sin(-sumspeed[numneedle - 1]) + height / 2;
				setcolor(BLUE);
				line(width / 2, height / 2, XEND, YEND);
				for (int i = 0; i < numneedle; i++) {
					if (abs(sumspeed[numneedle - 1] - sumspeed[numneedle]) < pi / 60) {
						ratespeed = 0;
						break;
					}
				}
				score += 1;
			}
		}
	}
	closegraph();
	return 0;
}