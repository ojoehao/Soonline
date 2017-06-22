# _*_ coding: utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg,CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from forms import AskUserForm
from courses.models import Course
from operation.models import UserFavorite
# Create your views here.


class OrgView(View):
    """
    课程列表功能
    """
    def get(self, request):
        #课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        #城市
        all_citys = CityDict.objects.all()
        city_id = request.GET.get('city', "")
        ct = request.GET.get('ct',"")
        sort = request.GET.get('sort', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        if ct:
            all_orgs = all_orgs.filter(category=ct)
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")
        #课程数量
        orgs_num = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html',{
            "orgs":orgs,
            "hot_orgs":hot_orgs,
            "all_citys":all_citys,
            "orgs_num":orgs_num,
            "city_id":city_id,
            "ct":ct,
            "sort":sort,
            "menu_typ":"skjg",
        })


class AddAskUserView(View):
    """
    用户添加咨询
    
    """
    def post(self,request):
        askuser_form = AskUserForm(request.POST)
        if askuser_form.is_valid():
            ask_user = askuser_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错!"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构详情首页
    """
    def get(self,request,org_id):
        cur_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request,'org-detail-homepage.html',{
            "all_courses":all_courses,
            "all_teachers":all_teachers,
            "course_org":course_org,
            "cur_page":cur_page,
            "has_fav":has_fav,
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self,request,org_id):
        cur_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        return render(request,'org-detail-course.html',{
            "all_courses":all_courses,
            "course_org":course_org,
            "cur_page":cur_page,
            "has_fav": has_fav,
        })


class OrgDescView(View):
    """
    机构详情描述页
    """
    def get(self,request,org_id):
        cur_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-desc.html',{
            "course_org":course_org,
            "cur_page":cur_page,
            "has_fav": has_fav,
        })


class OrgTeacherView(View):
    """
    机构教师列表页
    """
    def get(self,request,org_id):
        cur_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request,'org-detail-teachers.html',{
            "all_teachers":all_teachers,
            "course_org":course_org,
            "cur_page":cur_page,
            "has_fav": has_fav,
        })


class AddFavView(View):
    """
    用户添加/取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id','')
        fav_type = request.POST.get('fav_type','')

        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录，请先登录!"}', content_type='application/json')
        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_record:
            #如果记录已经存在， 则表示用户取消收藏
            exist_record.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.user = request.user
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错！"}', content_type='application/json')


