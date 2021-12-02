#include <windows.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include <wchar.h>
#include <strsafe.h>
#include "systems.h"



LRESULT WINAPI Winproc(HWND hwnd,UINT message,WPARAM wparam,LPARAM lparam)
{
	HDC hdc;                            //当前窗口句柄
	PAINTSTRUCT ps;                          //画图结构
	//RECT rect;
	//CHAR msg[100];
	TCHAR mm[20];
	size_t lentrg;                            //textout文字输入时需要获取文字长度
	TEXTMETRIC tm;
	static UINT cxwidth,cyheight,cxcpas,cxclient,cyclient,ivscollpostion;                   //定义字体的x跟y轴的方位坐标
	switch(message)
	{
		case WM_VSCROLL:
			hdc = GetDC(hwnd);
			switch(LOWORD(wparam))
			{
				/*case SB_BOTTOM:          //滚动底部事件
					TextOut(hdc,100,100,L"滚动到了底部",lstrlen(L"滚动到了底部"));
					break;
				case SB_TOP:              //滚动顶部事件
					TextOut(hdc,100,100,L"滚动到了顶部",lstrlen(L"滚动到了顶部"));
					break;*/
				case SB_LINEUP:
					ivscollpostion -= 1;
					//TextOut(hdc,cxclient / 2,cyclient / 2,L"向上翻了一行",lstrlen(L"向上翻了一行"));
					break;
				case SB_LINEDOWN:
					ivscollpostion += 1;
					//TextOut(hdc,cxclient / 2,cyclient / 2,L"向下翻了一行",lstrlen(L"向下翻了一行"));
					break;
				case SB_PAGEUP:           //向上翻了一页
					ivscollpostion -= cxclient / cxwidth;
					//TextOut(hdc,cxclient / 2,cyclient / 2,L"向上翻了一页",lstrlen(L"向上翻了一页"));
					break;
				case SB_PAGEDOWN:
					ivscollpostion += cxclient / cxwidth;
					//TextOut(hdc,cxclient / 2,cyclient / 2,L"向下翻了一页",lstrlen(L"向下翻了一页"));
					break;
				case SB_THUMBPOSITION:
					ivscollpostion = HIWORD(wparam);
					//TextOut(hdc,cxclient / 2,cyclient / 2,L"按住不放!!",lstrlen(L"按住不放!!"));
					break;
			}
			ivscollpostion = max(0,min(ivscollpostion,NUMS -1));
			if(ivscollpostion != GetScrollPos(hwnd,SB_VERT))                //进行判断当前滑块位置跟之前的滑块位置进行比较，不一样是就进行重新设置滑块的位置
			{
				SetScrollPos(hwnd,SB_VERT,ivscollpostion,TRUE);
				InvalidateRect(hwnd,NULL,TRUE);
			}
			ReleaseDC(hwnd,hdc);
			return 0;

		case WM_SIZE:
			cxclient = LOWORD(lparam);
			cyclient = HIWORD(lparam);
			/*hdc = GetDC(hwnd);
			StringCchPrintf(mm,20,L"窗口大小是%5d * %5d",LOWORD(lparam),HIWORD(lparam));
			StringCchLength(mm,20,&lentrg);
			TextOut(hdc,100,100,mm,lentrg);
			ReleaseDC(hwnd,hdc);*/
			return 0;
		case WM_PAINT:
			hdc = BeginPaint(hwnd,&ps);

			/*GetClientRect(hwnd,&rect);
			DrawText(hdc,L"我的第一个程序",-1,&rect,DT_SINGLELINE | DT_CENTER | DT_VCENTER);
			StringCchLength(mm,6,&lentrg);
			TextOut(hdc,0,0,mm,lentrg);
			for(int i=0;i<8;i++)
			{
				StringCchPrintf(msg,10,L"%d\t%s",i+1,L"我的第一个程序");
				StringCchLength(msg,10,&lentrg);
				TextOut(hdc,cxwidth,(i+1) * cyheight,msg,lentrg);
			}*/
			int y;
			for(int i=0;i<NUMS;i++)
			{
				y = cyheight * (i - ivscollpostion);
				TextOut(hdc,0,y,sysmetrics[i].szLabel,lstrlen(sysmetrics[i].szLabel));
				TextOut(hdc,22 * cxcpas,y,sysmetrics[i].szDesc,lstrlen(sysmetrics[i].szDesc));
				SetTextAlign(hdc,TA_RIGHT | TA_TOP);
				StringCchPrintf(mm,10,L"%5d",GetSystemMetrics(sysmetrics[i].Inedx));                     //GetSystemMetrics得到系统的像素内容
				StringCchLength(mm,10,&lentrg);
				TextOut(hdc,22 * cxcpas + 40 * cxwidth,y,mm,lentrg);
				SetTextAlign(hdc,TA_LEFT | TA_TOP);
			}

			EndPaint(hwnd,&ps);
			return 0;
		case WM_CREATE:
			hdc = GetDC(hwnd);
			GetTextMetrics(hdc,&tm);
			cxclient = LOWORD(lparam);
			cyclient = HIWORD(lparam);
			cxwidth = tm.tmAveCharWidth;
			cyheight = tm.tmExternalLeading + tm.tmHeight;
			cxcpas = (tm.tmPitchAndFamily | 1 ? 3 : 2) * cxwidth /2;
			SetScrollRange(hwnd,SB_VERT,0,NUMS - 1,TRUE);
			SetScrollPos(hwnd,SB_VERT,ivscollpostion,TRUE);
			ReleaseDC(hwnd,hdc);
			//MessageBox(NULL,L"程序错误",L"我的程序",MB_OK);
			return 0;
		case WM_CLOSE:
			if(MessageBox(NULL,L"是否关闭程序?",L"关闭程序",MB_YESNO)== IDYES)
				DestroyWindow(hwnd);
			else
				return 0;
		case WM_LBUTTONDOWN:
			MessageBox(NULL,L"点击了屏幕",L"点击",MB_OK);
			return 0;
		case WM_DESTROY:
			PostQuitMessage(0);
			return 0;
	}
	return DefWindowProc(hwnd,message,wparam,lparam);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow )
{
	wchar_t szappname[20] = L"biechaibaik";
	MSG msg;
	HWND hwnd;
	WNDCLASS wndclass;
	wndclass.cbClsExtra = 0;
	wndclass.cbWndExtra = 0;
	wndclass.hInstance = hInstance;
	//wndclass.hbrBackground = (HBRUSH)GetSocketObject(WHITE_BRUSH);
	wndclass.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
	wndclass.hCursor = LoadCursor(NULL,IDC_ARROW);
	//wndclass.hIcon = LoadIcon(hInstance,MAKEINTRESOURCE(IDI_MYICON1));
	wndclass.hIcon = LoadIcon(NULL,IDI_APPLICATION);
	wndclass.lpfnWndProc = Winproc;
	wndclass.lpszClassName = szappname;
	wndclass.lpszMenuName = NULL;
	wndclass.style = CS_HREDRAW | CS_VREDRAW;

	RegisterClass(&wndclass);

	hwnd = CreateWindow(szappname,L"我的程序",WS_OVERLAPPEDWINDOW | WS_VSCROLL,CW_USEDEFAULT,CW_USEDEFAULT,600,500,NULL,NULL,hInstance,NULL);
	
	ShowWindow(hwnd,nCmdShow);
	UpdateWindow(hwnd);
	
	while(GetMessage(&msg,NULL,0,0))
	{
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}
	return msg.wParam;
}





