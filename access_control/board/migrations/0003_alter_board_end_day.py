# Generated by Django 3.2.8 on 2021-10-24 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_alter_board_start_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='end_day',
            field=models.DateField(verbose_name='종료날짜'),
        ),
    ]
