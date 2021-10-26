from django import forms
from django.forms.widgets import NumberInput

class BoardForm(forms.Form):
    start_date = forms.DateField(
        error_messages={
            'required': '시작일을 입력해주세요'
        },
        widget=NumberInput(attrs={'type': 'date'}), label="시작일")
    end_date = forms.DateField(
        widget=NumberInput(attrs={'type': 'date'}), required=False, label="종료일")
    company = forms.CharField(
        error_messages={
            'required': '업체명을 입력해주세요'
        },
        max_length=128, label="업체명")
    position = forms.CharField(
        error_messages={
            'required': '직책을 입력해주세요'
        },
        max_length=128, label="직책")
    guest_name = forms.CharField(
        error_messages={
            'required': '이름을 입력해주세요'
        },
        max_length=32, label="이름")