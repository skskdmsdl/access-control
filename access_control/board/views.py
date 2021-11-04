from django.shortcuts import render, redirect
from .models import Board
from datetime import datetime
from .forms import BoardForm
from django.http import HttpResponse
from datetime import datetime

import xlwt
import locale

# Create your views here.

# home 추가
def home(request):
    
    return render(request, 'home.html')

# excel 다운로드
def excel_export(request):

    locale.setlocale(locale.LC_ALL,'')
    today = datetime.today().strftime('%Y-%m-%d')
    todayValue = datetime.today().strftime('%Y-%m-%d (%a)')
	
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\'example.xls' 
    wb = xlwt.Workbook(encoding='ansi') #encoding은 ansi로 해준다.
    ws = wb.add_sheet('출입 신청', cell_overwrite_ok=True) #시트 추가 및 overwrite true 설정
    
    row_num = 0
    col_names = ['번호', '날짜', '업체명', '직책', '이름']
    
    # 테두리 설정
    style = xlwt.XFStyle()
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    style.borders = borders

    #열이름을 첫번째 행에 추가 시켜준다.
    for idx, col_name in enumerate(col_names):
    	ws.write(row_num, idx, col_name, style)
        
    #데이터 베이스에서 유저 정보를 불러온다.
    # rows = Board.objects.all().values_list('start_date', 'company', 'position', 'guest_name') 
    rows = Board.objects.filter(start_date__gte = today, end_date__lte = today).values_list('start_date', 'start_date', 'company', 'position', 'guest_name')
    
    # 날짜 서식으로 변경
    date_format = xlwt.XFStyle()
    date_format.borders = borders
    date_format.num_format_str = 'yyyy-mm-dd (aaa)'

    #유저정보를 한줄씩 작성한다.
    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], style)
            ws.write(row_num, 0, row_num, style)
            ws.write(row_num, 1, todayValue, date_format)
            ws.col(1).width = 25*255
            
    wb.save(response)
    
    return response

def board_write(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            
            board = Board()
            board.start_date = form.cleaned_data['start_date']
            board.end_date = form.cleaned_data['end_date']
            board.company = form.cleaned_data['company']
            board.position = form.cleaned_data['position']
            board.guest_name = form.cleaned_data['guest_name']
            board.save()

            return redirect('/board/list/')
    else:
        form = BoardForm()
    
    return render(request, 'board_write.html', {'form': form})


def board_list(request):
    boards = Board.objects.all().order_by('-id')
    return render(request, 
                'board_list.html', 
                {'boards': boards, 'time' : datetime.now()},)