from django.urls import path
from . import views

urlpatterns = [
    # path('detail/<int:pk>/delete', views.delete, name='delete'),
    path('detail/<int:pk>/update', views.update, name='update'),
    path('detail/<int:pk>/', views.board_detail, name='detail'),
    path('list/', views.board_list),
    path('write/', views.board_write),
    path(r'^export/xls/$', views.excel_export, name='excel_export')
]