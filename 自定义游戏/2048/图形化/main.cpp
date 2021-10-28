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
#include <ctime>
#include <cstdlib>
#include <graphics.h>	//EGE graphic library
#define MAX_GRID 4
#define GRID 125
#define k 20
#define Random rand() % 4
using namespace std;

void Generate();
void initDraw();
void Draw();
void up();
void down();
void left();
void right();


enum color {
	c0 = EGERGB(221, 191, 216),     // ����ɫ  0
	c1  = EGERGB(161, 150, 216),        //2
	c2 = EGERGB(221, 181, 135),         //4
	c3 = EGERGB(255, 215, 0),			//8
	c4 = EGERGB(255, 165, 0),          //16
	c5 = EGERGB(255, 99, 71),          //32
	c6 = EGERGB(255, 69, 0),           //64
	c7 = EGERGB(178, 34, 34),            //128
	c8 = EGERGB(112, 54, 34),             //256
	c9 = EGERGB(190, 30, 50),             //512
	c10 = EGERGB(20, 60, 54),             //1024
	c11 = EGERGB(52, 61, 166),            //2048
	back = EGERGB(0xFC, 0xFC, 0XFC),    //����ɫ

};

color Color[] = {c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, back};

int num[] = {0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048};

int map[MAX_GRID][MAX_GRID] = {0};
int Recode[MAX_GRID][MAX_GRID];
int randx, randy;

POINT pxy[MAX_GRID][MAX_GRID];


int main() {
	const int width = k * 5 + GRID * MAX_GRID, height =  k * 5 + GRID * MAX_GRID;
	initgraph(width, height);
	setbkcolor(back);
	cleardevice();
	while (1) {
		initDraw();
		Draw();
		if (!kbhit()) {
			char input = getch();
			switch (input) {
				case 'w':
					up();
					break;
				case 's':
					down();
					break;
				case 'a':
					left();
					break;
				case 'd':
					right();
					break;
			}
		}
	}
	return 0;
}


void initDraw() {
	for (int i = 0; i < MAX_GRID; i++) {
		for (int j = 0; j < MAX_GRID; j++) {
			pxy[i][j].x = j * GRID + (j + 1) * k;
			pxy[i][j].y = i * GRID + (i + 1) * k;
		}
	}
}

void Draw() {
	Generate();
	char s[10];
	for (int i = 0; i < MAX_GRID; i++) {
		for (int j = 0; j < MAX_GRID; j++) {
			for (int q = 0; q < 12; q++) {
				if (map[i][j] = num[q]) {
					setfillcolor(Color[q]);
					bar(pxy[i][j].x, pxy[i][j].y, pxy[i][j].x + GRID, pxy[i][j].y + GRID);
				}
			}
			if (map[i][j] != 0) {
				itoa(map[i][j], s, 10);
				outtextxy(pxy[i][j].x, pxy[i][j].y, s);
			}
		}
	}
}

void Generate() {
	for (int i; i < MAX_GRID; i++) {
		for (int j = 0; j < MAX_GRID; j++) {
			if (map[i][j] == 0) {
				Recode[i][j] = map[i][j];
			}
		}
	}
	randx = Random;
	randy = Random;
	map[randx][randy] = 2;
}

void up() {
	for (int i = 0; i < MAX_GRID; i++) {
		for (int j = 1, h = 0; j >= 0; j++) {
			if (map[j][i] > 0) {
				if (map[j][i] == map[h][i]) {
					map[h][i] *= 2;
					map[j][i] = 0;
				} else if (map[h][i] == 0) {
					map[h][i] = map[j][i];
					map[j][i] = 0;
					h += 1;
				}
			}
		}
	}
}


void down() {
	int i = 1;
}

void left() {
	int i = 1;
}

void right() {
	int i = 1;
}