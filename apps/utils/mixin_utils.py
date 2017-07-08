# _*_ coding: utf-8 _*_
__author__ = 'Joe'
__date = '17/7/7 下午9:46'


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/', redirect_field_name='redirect_to'))
    def dispatcher(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatcher(request, *args, **kwargs)