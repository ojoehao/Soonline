# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from organization.models import CourseOrg,Teacher
# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"所属课程机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(choices=(("cj", u"初级"), ("zj", u"中级"), ("gj", u"高级")), max_length=3,verbose_name=u"难度")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    category = models.CharField(max_length=100, verbose_name=u"课程类别", null=True, blank=True)
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    add_time= models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    tag = models.CharField(default="", max_length=10, verbose_name=u"课程标签")
    uneed_know = models.CharField(default="", max_length=10, verbose_name=u"课程须知")
    teacher_tell = models.CharField(default="", max_length=10, verbose_name=u"老师告诉你")
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播图")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name


    def __unicode__(self):
        return self.name

    #获取课程章节数
    def get_zj_nums(self):
        return self.lesson_set.all().count()

    #获取课程学生(显示5个)
    def get_course_student(self):
        return self.usercourse_set.all()[:5]


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=50, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(max_length=50, verbose_name=u"视频名")
    url = models.CharField(max_length=50, verbose_name=u"访问地址", default="")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=50, verbose_name=u"课程资源名")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name