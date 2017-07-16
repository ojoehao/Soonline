# _*_ coding: utf-8 _*_
__author__ = 'Joe'
__date = '17/6/3 下午9:16'
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','birthday','mobile','gender','address']