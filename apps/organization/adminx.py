# _*_ coding: utf-8 _*_
__author__ = 'Joe'
__date = '17/5/31 下午11:07'
import xadmin

from .models import CityDict,CourseOrg,Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc','category', 'click_nums','fav_nums','image','address','city','add_time']
    search_fields = ['name', 'desc','category',  'click_nums','fav_nums','image','address','city']
    list_filter = ['name', 'desc', 'category', 'click_nums','fav_nums','image','address','city','add_time']


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years','work_company','work_position','points','click_nums','fav_nums','add_time']
    search_fields = ['name', 'org', 'work_years','work_company','work_position','points','click_nums','fav_nums']
    list_filter = ['name', 'org', 'work_years','work_company','work_position','points','click_nums','fav_nums','add_time']


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)
