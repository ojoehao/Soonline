# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponse
from .models import Course,CourseResource
from operation.models import UserFavorite,CourseComments,UserCourse
from datetime import datetime
from django.db.models import Q
#from utils.mixin_utils import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class CourseView(View):
    """
    课程列表功能
    """
    def get(self, request):
        #课程
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = all_courses.order_by("-click_nums")[:3]

        #全局搜索keyword
        search_keyword = request.GET.get('keywords', "")
        if search_keyword:
            all_courses = all_courses.filter(Q(name__icontains=search_keyword) | Q(desc__icontains=search_keyword) | Q(detail__icontains=search_keyword))
        #排序
        city_id = request.GET.get('city', "")
        ct = request.GET.get('ct',"")
        sort = request.GET.get('sort', "")
        if city_id:
            all_courses = all_courses.filter(city_id=int(city_id))
        if ct:
            all_courses = all_courses.filter(category=ct)
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
            "search_keyword": search_keyword,
            "selectOption": "公开课",
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


class CourseInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    """
        课程章节信息
    """

    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        #学习人数加1
        course.students += 1
        course.save()
        #查询用户是否已经关联该课程
        user_course = UserCourse.objects.filter(user=request.user,course=course)
        if not user_course:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

        #相关资源下载
        all_resourses = CourseResource.objects.filter(course=course)
        #该课的同学还学过 relate_courses
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        return render(request,'course-video.html',{
            "course":course,
            "all_resourses":all_resourses,
            "relate_courses":relate_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    """
        课程评论信息
    """

    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_resourses = CourseResource.objects.filter(course=course)
        course_comments = course.coursecomments_set.all()
        # 该课的同学还学过 relate_courses
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(course_comments, 10, request=request)
        course_comments = p.page(page)
        return render(request,'course-comment.html',{
            "course":course,
            "all_resourses":all_resourses,
            "course_comments":course_comments,
            "relate_courses": relate_courses,
        })


class CourseAddCommentView(View):
    """
    添加课程评论信息
    """
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录，请先登录!"}', content_type='application/json')
        course_id = request.POST.get("course_id",0)
        comments = request.POST.get("comments","")
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.comments = comments
            course_comments.course = course
            course_comments.user = request.user
            course_comments.add_time = datetime.now()
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功!"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败!"}', content_type='application/json')




