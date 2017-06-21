# _*_ coding: utf-8 _*_
__author__ = 'Joe'
__date = '17/6/3 下午9:16'
from django import forms
import re

from operation.models import AskUser


class AskUserForm(forms.ModelForm):

    class Meta:
        model = AskUser
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        :return: 
        """
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[358]\d{9}$|147\d{8}$|176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法",code="mobile_invaild")