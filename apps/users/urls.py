# _*_ coding: utf-8 _*_
__author__ = 'Joe'
__date = '17/6/18 下午1:58'
from django.conf.urls import url, include
from users.views import UserInfoView, UploadImageView, ModifyPwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, \
    MyFavOrgView, MyFavCourseView, MyFavTeacherView, MyMessageView

urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),
    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    # 个人中心修改密码
    url(r'^update/pwd/$', ModifyPwdView.as_view(), name="update_pwd"),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name="sendemail_code"),
    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
    # 我的课程
    url(r'^my_course/$', MyCourseView.as_view(), name="my_course"),
    # 我收藏的机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),
    # 我收藏的课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),
    # 我收藏的教师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),
    # 我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name="mymessage"),

    # url(r'^detl/(?P<course_id>\d+)/$', CourseDetlView.as_view(), name="course_detl"),
    # url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    # url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comment"),
    # url(r'^add_comment/$', CourseAddCommentView.as_view(), name="course_add_comment"),
]
