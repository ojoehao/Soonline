# _*_ coding: utf-8 _*_
__author__ = 'Joe'
__date = '17/6/18 下午1:58'
from django.conf.urls import url, include
from courses.views import CourseView,CourseDetlView,CourseInfoView,CourseCommentView,CourseAddCommentView

urlpatterns = [
    #课程机构首页
    url(r'^list/$', CourseView.as_view(), name="course_list"),
    url(r'^detl/(?P<course_id>\d+)/$', CourseDetlView.as_view(), name="course_detl"),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comment"),
    url(r'^add_comment/$', CourseAddCommentView.as_view(), name="course_add_comment"),
]