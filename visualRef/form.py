from django import forms

#注册框，register
class rForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()
    email=forms.EmailField()

#登录框，login
class lForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

#个人信息框，profile
class pForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    bio=forms.CharField(max_length=500)
    company=forms.CharField(max_length=100)
    location=forms.CharField(max_length=100)
    birth_date=forms.DateField()