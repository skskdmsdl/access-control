# Generated by Django 3.2.8 on 2021-10-26 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_alter_board_end_day'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='end_day',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='board',
            old_name='start_day',
            new_name='start_date',
        ),
    ]
