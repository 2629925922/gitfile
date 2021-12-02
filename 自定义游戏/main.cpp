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
	HDC hdc;                            //��ǰ���ھ��
	PAINTSTRUCT ps;                          //��ͼ�ṹ
	//RECT rect;
	//CHAR msg[100];
	TCHAR mm[20];
	size_t lentrg;                            //textout��������ʱ��Ҫ��ȡ���ֳ���
	TEXTMETRIC tm;
	static UINT cxwidth,cyheight,cxcpas,cxclient,cyclient,ivscollpostion;                   //���������x��y��ķ�λ����
	switch(message)
	{
		case WM_VSCROLL:
			hdc = GetDC(hwnd);
			switch(LOWORD(wparam))
			{
				/*case SB_BOTTOM:          //�����ײ��¼�
					TextOut(hdc,100,100,L"�������˵ײ�",lstrlen(L"�������˵ײ�"));
					break;
				case SB_TOP:              //���������¼�
					TextOut(hdc,100,100,L"�������˶���",lstrlen(L"�������˶���"));
					break;*/
				case SB_LINEUP:
					ivscollpostion -= 1;
					//TextOut(hdc,cxclient / 2,cyclient / 2,L"���Ϸ���һ��",lstrlen(L"���Ϸ���һ��"));
					break;
				case SB_LINEDOWN:
					ivscollpostion += 1;
					//TextOut(hdc,cxclient / 2,cyclient / 2,L"���·���һ��",lstrlen(L"���·���һ��"));
					break;
				case SB_PAGEUP:           //���Ϸ���һҳ
					ivscollpostion -= cxclient / cxwidth;
					//TextOut(hdc,cxclient / 2,cyclient / 2,L"���Ϸ���һҳ",lstrlen(L"���Ϸ���һҳ"));
					break;
				case SB_PAGEDOWN:
					ivscollpostion += cxclient / cxwidth;
					//TextOut(hdc,cxclient / 2,cyclient / 2,L"���·���һҳ",lstrlen(L"���·���һҳ"));
					break;
				case SB_THUMBPOSITION:
					ivscollpostion = HIWORD(wparam);
					//TextOut(hdc,cxclient / 2,cyclient / 2,L"��ס����!!",lstrlen(L"��ס����!!"));
					break;
			}
			ivscollpostion = max(0,min(ivscollpostion,NUMS -1));
			if(ivscollpostion != GetScrollPos(hwnd,SB_VERT))                //�����жϵ�ǰ����λ�ø�֮ǰ�Ļ���λ�ý��бȽϣ���һ���Ǿͽ����������û����λ��
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
			StringCchPrintf(mm,20,L"���ڴ�С��%5d * %5d",LOWORD(lparam),HIWORD(lparam));
			StringCchLength(mm,20,&lentrg);
			TextOut(hdc,100,100,mm,lentrg);
			ReleaseDC(hwnd,hdc);*/
			return 0;
		case WM_PAINT:
			hdc = BeginPaint(hwnd,&ps);

			/*GetClientRect(hwnd,&rect);
			DrawText(hdc,L"�ҵĵ�һ������",-1,&rect,DT_SINGLELINE | DT_CENTER | DT_VCENTER);
			StringCchLength(mm,6,&lentrg);
			TextOut(hdc,0,0,mm,lentrg);
			for(int i=0;i<8;i++)
			{
				StringCchPrintf(msg,10,L"%d\t%s",i+1,L"�ҵĵ�һ������");
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
				StringCchPrintf(mm,10,L"%5d",GetSystemMetrics(sysmetrics[i].Inedx));                     //GetSystemMetrics�õ�ϵͳ����������
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
			//MessageBox(NULL,L"�������",L"�ҵĳ���",MB_OK);
			return 0;
		case WM_CLOSE:
			if(MessageBox(NULL,L"�Ƿ�رճ���?",L"�رճ���",MB_YESNO)== IDYES)
				DestroyWindow(hwnd);
			else
				return 0;
		case WM_LBUTTONDOWN:
			MessageBox(NULL,L"�������Ļ",L"���",MB_OK);
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

	hwnd = CreateWindow(szappname,L"�ҵĳ���",WS_OVERLAPPEDWINDOW | WS_VSCROLL,CW_USEDEFAULT,CW_USEDEFAULT,600,500,NULL,NULL,hInstance,NULL);
	
	ShowWindow(hwnd,nCmdShow);
	UpdateWindow(hwnd);
	
	while(GetMessage(&msg,NULL,0,0))
	{
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	}
	return msg.wParam;
}





