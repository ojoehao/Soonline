# _*_ coding: utf-8 _*_
__author__ = 'Joe'
__date = '17/5/31 下午10:34'
import xadmin
from xadmin import views

from .models import EmailVerifyRecord,Banner,UserProfile


class BaseSetting(object):
    enable_themes= True
    use_bootswatch = True


class GrobalSetting(object):
    site_title = u"So学网后台管理系统"
    site_footer = u"So学在线学习平台"
    menu_style = "accordion"

    # 菜单设置
    def get_site_menu(self):
        return (
            {'title': '用户管理', 'perm': self.get_model_perm(UserProfile, 'change'), 'menus': (
                {'title': '用户信息', 'icon': 'fa fa-vimeo-square'
                    , 'url': self.get_model_url(UserProfile, 'changelist')},
                {'title': '邮箱验证码', 'icon': 'fa fa-vimeo-square'
                    , 'url': self.get_model_url(EmailVerifyRecord, 'changelist')},
                {'title': '轮播图', 'icon': 'fa fa-vimeo-square'
                    , 'url': self.get_model_url(Banner, 'changelist')},

            )},
        )


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']


class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title','image','url','index']
    list_filter = ['title','image','url','index','add_time']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GrobalSetting)