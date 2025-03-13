from django import forms

class UserInfoForm(forms.Form):
 first_name=forms.CharField(label="Ім'я",max_length=100)
 last_name=forms.CharField(label='Прізвище',max_length=100)
 phone=forms.CharField(label='Телефон',max_length=15)

class BookingDetailsForm(forms.Form):
 barber=forms.IntegerField(widget=forms.HiddenInput(),required=False)
 service=forms.IntegerField(widget=forms.HiddenInput(),required=False)
 date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}),required=False)
 time=forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}),required=False)
