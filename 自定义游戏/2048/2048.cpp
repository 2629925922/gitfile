#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <stdbool.h>
#include <string.h>

#define SIZE 4
#define random(x) rand()%x


int map[4][4] = { 0 };
void print_map();
void randvalue();
bool judge();
void init();
struct spares
{
	int nums[2];
}spare[16];

//void getcommand(char command);

int main()
{
	bool res = true;
	char command;
	while (res)
	{
		print_map();
		if (!_kbhit())
		{
			command = _getch();
		}
		res = judge();
		system("cls");
	}
	printf("游戏结束\n%d", spare[0].nums[0]);
	return 0;
}

void print_map()
{
	printf("2048小游戏\n");
	printf("w是上，s是下，a是左，d是右\n");
	randvalue();
	for (int i = 0; i < SIZE; i++)
	{
		for (int j = 0; j < SIZE; j++)
		{
			printf("%5d", map[i][j]);
			if (j == 3) printf("\n");
		}
	}
}

void randvalue()
{
	//	bool ii = true;
	int x_new, y_new, jjj;
	int iii = 0;
	//	while(ii)
	//	{	
	//		x_new = random(3),y_new =random(3);
	//		if(map[x_new][y_new] == 0)
	//		{
	//			map[x_new][y_new] = 2;
	//			ii=false;
	//		}
	//	}
	struct spares spare[16] = { 0 };
	for (int i = 0; i < SIZE; i++)
	{
		for (int j = 0; j < SIZE; j++)
		{
			if (map[i][j] == 0) spare[iii++] = { i,j };
		}
	}
	printf("\n");
	jjj = random(iii);
	x_new = spare[jjj].nums[0];
	y_new = spare[jjj].nums[1];
	map[x_new][y_new] = 2;
}

bool judge()
{
	if (map[spare[0].nums[0]][spare[0].nums[1]] != 0) return false;
	return true;
}