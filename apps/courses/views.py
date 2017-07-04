# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .models import Course
from operation.models import UserFavorite
# Create your views here.


class CourseView(View):
    """
    课程列表功能
    """
    def get(self, request):
        #课程
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = all_courses.order_by("-click_nums")[:3]
        city_id = request.GET.get('city', "")
        ct = request.GET.get('ct',"")
        sort = request.GET.get('sort', "")
        if city_id:
            all_orgs = all_courses.filter(city_id=int(city_id))
        if ct:
            all_orgs = all_courses.filter(category=ct)
        if sort:
            if sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
            elif sort == "students":
                all_courses = all_courses.order_by("-students")
        #课程数量
        courses_num = all_courses.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html',{
            "courses":courses,
            "hot_courses":hot_courses,
            "courses_num":courses_num,
            "city_id":city_id,
            "ct":ct,
            "sort":sort,
            "menu_typ":"gkk",
        })


class CourseDetlView(View):
    """
    课程详情页
    """
    def get(self,request,course_id):
        cur_page = "detail"
        has_course_fav = False
        has_org_fav = False
        course = Course.objects.get(id=int(course_id))
        # 点击数
        course.click_nums += 1
        course.save()
        relate_courses = ''
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_course_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_org_fav = True
        return render(request,'course-detail.html',{
            "course":course,
            "has_course_fav":has_course_fav,
            "has_org_fav":has_org_fav,
            "relate_courses": relate_courses,
        })


class CourseInfoView(View):
    """
    课程章节信息
    """
    def get(self,request,course_id):
        cur_page = "detail"
        course = Course.objects.get(id=int(course_id))
        return render(request,'course-video.html',{
            "course":course,
        })


