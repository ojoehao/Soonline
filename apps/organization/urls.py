# _*_ coding: utf-8 _*_
__author__ = 'Joe'
__date = '17/6/18 下午1:58'
from django.conf.urls import url, include
from organization.views import OrgView,AddAskUserView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFavView,TeacherView,TeacherDetlView


urlpatterns = [
    #课程机构首页
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddAskUserView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org_course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org_desc"),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org_teacher"),
    #机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

    #讲师列表页
    url(r'^teacher/list/$', TeacherView.as_view(), name="teacher_list"),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetlView.as_view(), name="teacher_detail"),
]