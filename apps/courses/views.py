# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .models import Course
# Create your views here.


class CourseView(View):
    """
    课程列表功能
    """
    def get(self, request):
        #课程机构
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
