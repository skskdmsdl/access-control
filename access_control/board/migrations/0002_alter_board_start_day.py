# Generated by Django 3.2.8 on 2021-10-24 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='start_day',
            field=models.DateField(verbose_name='시작날짜'),
        ),
    ]
