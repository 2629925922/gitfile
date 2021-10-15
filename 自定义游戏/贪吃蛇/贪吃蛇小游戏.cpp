#include <stdio.h>
#include <time.h>
#include <conio.h>
#include <stdlib.h> 
#define size 19
 
void init(int *length,int maps[size][size]);            //定义初始地图函数 
void draw(int[size][size]);
int getcommand(int dir);
int move(int command,int *length,int maps[size][size]);

int main()
{
	int map[size][size] = {0},length = 0,result,dir;
	init(&length,map);
	while(1)
	{
		system("cls");
		draw(map);
		int nums = getcommand(dir);
		result = move(nums,&length,map);
		if(result == 1)
		{
			printf("你已死亡，游戏结束!!!");
			break;
		}
		if(result == 2)
		{
			printf("游戏胜利!!!");
			break;
		}
	}
	system("pause");
	return 0; 
}

void init(int *length,int maps[size][size])
{
	int food=-1,a=rand(),b=rand();
	maps[2][1] = 1;
	maps[1][1] = 2;
	maps[0][1] = 3;
	maps[5][3] = food;
	*length = 3;
}

void draw(int maps[size][size])
{
	for(int i=0;i<19;i++)
	{
		for(int j=0;j<19;j++)
		{
			printf("%d",maps[i][j]);
			if(j==18) printf("\n");
		}
	}
	printf("\n");
}

int getcommand(int dir)
{
	int num=dir;char command = getch();
	if(command)
	{
		switch(command)
		{
			case 'w' : num = 0;break;      //向上
			case 's' : num = 1;break;      //向下
			case 'a' : num = 2;break;      //向左
			case 'd' : num = 3;break;      //向右 
			default : printf("程序错误，已退出");
		}
	}
	if(num - dir == 2 || num - dir == -2)
	{
		num = dir;
	}
	return num;
}

int move(int command,int *length,int maps[size][size])
{
	int head_i,head_j;
	for(int i=0;i<size;i++)
	{
		for(int j=0;j<size;j++)
		{
			if(maps[i][j]==*length)
			{
				maps[i][j] = 0;
			}
			else if(maps[i][j]>1)
			{
				maps[i][j] += 1; 
			}
			else if(maps[i][j]==1)
			{
				maps[i][j] += 1;
				switch(command)
				{
					case 0 : head_i = i - 1,head_j = j;break;
					case 1 : head_i = i + 1,head_j = j;break;
					case 2 : head_i = i,head_j = j - 1;break;
					case 3 : head_i = i,head_j = j + 1;break;
					default : printf("程序错误，已退出");break;
				}
			}
		}
	}
	if(maps[head_i][head_j] == -1)
	{
		return 2; 
	}
	else if(maps[head_i][head_j] > 0 || head_i == size || head_j == size)
	{	
		return 1;
	}
	else
	{
		maps[head_i][head_j]=1;
	}
	return 0;
}
