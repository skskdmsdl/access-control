from django.shortcuts import render, redirect
from .models import Board
from datetime import datetime
from .forms import BoardForm
from django.http import HttpResponse
from datetime import datetime
from django.http import Http404
from urllib.parse import quote

import io
import xlwt
import locale
import xlsxwriter


# Create your views here.

def update(request, pk):
    board = Board.objects.get(pk=pk)
    if request.method == 'POST':
        form = BoardForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            board.start_date = form.cleaned_data['start_date']
            board.end_date = form.cleaned_data['end_date']
            board.company = form.cleaned_data['company']
            board.position = form.cleaned_data['position']
            board.guest_name = form.cleaned_data['guest_name']
            board.save()
            return redirect('/board/detail/'+str(pk))
    else:
        return redirect('/board/detail/'+str(pk))

def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')

    return render(request, 'board_detail.html', {'board':board})

# home 추가
def home(request):
    
    return render(request, 'home.html')

# excel 다운로드
# def excel_export(request):

#     locale.setlocale(locale.LC_ALL,'')
#     today = datetime.today().strftime('%Y-%m-%d')
#     todayValue = datetime.today().strftime('%Y-%m-%d (%a)')
	
#     response = HttpResponse(content_type="application/vnd.ms-excel")
#     response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\'example.xls'
#     wb = xlwt.Workbook(encoding='ansi') #encoding은 ansi로 해준다.
#     ws = wb.add_sheet('출입 신청', cell_overwrite_ok=True) #시트 추가 및 overwrite true 설정
#     ws.col(0).width = 256 * 25

#     # 스타일 추가
#     style = xlwt.XFStyle()
#     alignment = xlwt.Alignment()
#     alignment.horz = xlwt.Alignment.HORZ_CENTER
#     style.alignment = alignment
#     font = xlwt.Font()
#     font.bold = True
#     style.font = font
    
#     # 첫번째 줄 추가
#     col_names = ['스마트 전자도서관시스템, 국회부산도서관 홈페이지 및 국회〮지방의회 의정정보시스템 개발사업 출입 신청']

#     for idx, col_name in enumerate(col_names):
#         ws.write_merge(0, 0, 0, 5, col_name, style)
#         # new_row_height = int(1000)
#         # ws.row(0).height = new_row_height
        

#     # 두번째 줄 추가
#     row_num = 1
#     col_names = ['순번', '기간', '업체명', '직급', '성명', '비고']
    
#     # 테두리 설정
#     style = xlwt.XFStyle()
#     borders = xlwt.Borders()
#     borders.left = 1
#     borders.right = 1
#     borders.top = 1
#     borders.bottom = 1
#     style.borders = borders
#     alignment = xlwt.Alignment()
#     alignment.horz = xlwt.Alignment.HORZ_CENTER
#     style.alignment = alignment

#     # 배경 색상 설정
#     pattern = xlwt.Pattern() 
#     pattern.pattern = xlwt.Pattern.SOLID_PATTERN
#     pattern.pattern_fore_colour = 22
#     # background = xlwt.easyxf('pattern: pattern solid, fore_color light_green')
#     pattern_style = xlwt.XFStyle()
#     pattern_style.pattern = pattern
#     pattern_style.borders = borders
#     alignment = xlwt.Alignment()
#     alignment.horz = xlwt.Alignment.HORZ_CENTER
#     pattern_style.alignment = alignment

#     #열이름을 두번째 행에 추가 시켜준다.
#     for idx, col_name in enumerate(col_names):
#     	ws.write(row_num, idx, col_name, pattern_style)
        
#     #데이터 베이스에서 유저 정보를 불러온다.
#     # rows = Board.objects.all().values_list('start_date', 'company', 'position', 'guest_name') 
#     rows = Board.objects.filter(start_date__lte = today, end_date__gte = today).values_list('start_date', 'end_date', 'company', 'position', 'guest_name', 'guest_name')
    
#     # 날짜 서식으로 변경
#     date_format = xlwt.XFStyle()
#     date_format.borders = borders
#     date_format.num_format_str = 'yyyy-mm-dd (aaa)'
#     alignment = xlwt.Alignment()
#     alignment.horz = xlwt.Alignment.HORZ_CENTER
#     date_format.alignment = alignment

#     #유저정보를 한줄씩 작성한다.
#     for row in rows:
#         row_num +=1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], style)
#             ws.write(row_num, 0, row_num-1, style)
#             ws.write(row_num, 1, todayValue, date_format)
#             # ws.write(row_num, 1, todayValue, date_format)
#             ws.write(row_num, 5, '', style)
#             ws.col(1).width = 20*255
#             ws.col(2).width = 20*255
#             ws.col(3).width = 15*255
#             ws.col(4).width = 15*255
#             ws.col(5).width = 20*255
            
            
#     wb.save(response)
    
#     return response

def get_simple_table_data():
    # Simulate a more complex table read.
    return [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]]

def excel_export(request):
    # Create an in-memory output file for the new workbook.
    output = io.BytesIO()

    # Even though the final file will be in memory the module uses temp
    # files during assembly for efficiency. To avoid this on servers that
    # don't allow temp files, for example the Google APP Engine, set the
    # 'in_memory' Workbook() constructor option as shown in the docs.
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    todayfilter = datetime.today().strftime('%Y-%m-%d')

    title = '스마트 전자도서관시스템, 국회부산도서관 홈페이지 및 국회〮지방의회 의정정보시스템 개발사업 출입 신청'

    worksheet.set_column('A:F', 12)
    worksheet.set_row(0, 57)

    merge_format = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter'})

    worksheet.merge_range('A1:F1', title, merge_format)

    # 
    row_num = 1
    col_names = ['순번', '기간', '업체명', '직급', '성명', '비고']
    for idx, col_name in enumerate(col_names):
     	worksheet.write(row_num, idx, col_name)

    # Get some data to write to the spreadsheet.
    # data = get_simple_table_data()
    data = Board.objects.filter(start_date__lte = todayfilter, end_date__gte = todayfilter).values_list('start_date', 'end_date', 'company', 'position', 'guest_name', 'guest_name')

    # Write some test data.
    for row_num, columns in enumerate(data):
        for col_num, cell_data in enumerate(columns):
            worksheet.write(row_num+2, col_num, cell_data)
            worksheet.write(row_num+2, 0, row_num+1)

    # Close the workbook before sending the data.
    workbook.close()

    # Rewind the buffer.
    output.seek(0)

    # Set up the Http response.
    today = datetime.today().strftime('%Y%m%d')
    filename = '출입신청_'+today+'.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = "attachment; filename*=UTF-8''{}".format(quote(filename.encode('utf-8')))

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