from django.shortcuts import render, redirect
from .models import Board
from datetime import datetime
from .forms import BoardForm
import xlwt


# Create your views here.

# excel 다운로드
def excel_export(request):
	
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\'example.xls' 
    wb = xlwt.Workbook(encoding='ansi') #encoding은 ansi로 해준다.
    ws = wb.add_sheet('참가자') #시트 추가
    
    row_num = 0
    col_names = ['email', 'name']
    
    #열이름을 첫번째 행에 추가 시켜준다.
    for idx, col_name in enumerate(col_names):
    	ws.write(row_num, idx, col_name)
        
    
    #데이터 베이스에서 유저 정보를 불러온다.
    rows = User.objects.all().values_list('name', 'email') 
    
    #유저정보를 한줄씩 작성한다.
    for row in rows:
    	row_num +=1
        for col_num, attr in enumerate(row):
        	ws.write(row_num, col_num, attr)
            
    wb.save(response)
    
    return reponse

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