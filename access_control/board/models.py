from django.db import models

# Create your models here.

class Board(models.Model):
    start_day = models.DateField(verbose_name='시작날짜')
    end_day = models.DateField(verbose_name='종료날짜')
    company = models.CharField(max_length=128,
                                verbose_name='업체명')
    position = models.CharField(max_length=128,
                                verbose_name='직책')
    guest_name = models.CharField(max_length=32,
                                verbose_name='출입자명')

    def __str__(self):
        return self.guest_name

    class Meta:
        db_table = 'board'
        verbose_name = '출입명단'
        verbose_name_plural = '출입명단' 
