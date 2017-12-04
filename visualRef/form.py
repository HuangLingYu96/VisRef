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