# _*_ coding: utf-8 _*_
import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import UserProfile, EmailVerifyRecord, Banner
from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg,Teacher
from forms import LoginForm,RegisterForm,ForgetPwdForm,ResetPwdForm,UploadImageForm,UserForm
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self,request):
        return render(request, "login.html", {})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户名未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误","login_form":login_form})
        else:
            return render(request, "login.html", {"login_form":login_form})


class LogoutView(View):
    """
    用户登出
    """
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                user = UserProfile.objects.get(email=record.email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form":register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_bound and not register_form.errors:
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"msg": "用户已经被注册","register_form":register_form})
            pass_word = request.POST.get("password", "")
            userProfile = UserProfile()
            userProfile.username = user_name
            userProfile.email = user_name
            userProfile.is_active = False
            userProfile.password = make_password(pass_word)
            userProfile.save()

            send_register_email(user_name,"register")
            # login(request, userProfile)
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form":register_form})


class ForgetPwdView(View):
    def get(self,request):
        forgetpsw_form = ForgetPwdForm()
        return render(request, "forgetpwd.html",{"forgetpsw_form":forgetpsw_form})

    def post(self,request):
        forgetpsw_form = ForgetPwdForm(request.POST)
        if forgetpsw_form.is_valid():
            email = request.POST.get("email","")
            send_register_email(email,"forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forgetpsw_form": forgetpsw_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "active_fail.html")


class ResetPwdView(View):
    def post(self,request):
        resetpwd_form = ResetPwdForm(request.POST)
        if resetpwd_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            email = request.POST.get("email","")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email":email, "msg":"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "resetpwd_form": resetpwd_form})


class UserInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    """
    用户个人信息
    """
    def get(self, request):
        return render(request, "usercenter-info.html", {
        })

    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse(json.dumps(user_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    """
    用户修改头像
    """

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class ModifyPwdView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    """
    个人中心修改密码
    """
    def post(self, request):
        resetpwd_form = ResetPwdForm(request.POST)
        if resetpwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            request.user.password = make_password(pwd1)
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(resetpwd_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    """
    个人中心修改邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经被注册!"}', content_type='application/json')
        send_register_email(email, "upd_email")
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    """
    个人中心修改邮箱
    """
    def post(self, request):
        code = request.POST.get('code', '')
        email = request.POST.get('email', '')
        exist_record = EmailVerifyRecord.objects.filter(email=email,code=code,send_type="upd_email")
        if exist_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误!"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    """
    我的课程
    """

    def get(self, request):
        my_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {
            "my_courses":my_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    """
    我的机构收藏
    """
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    """
    我的课程收藏
    """
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, "usercenter-fav-course.html", {
            "course_list": course_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    """
    我的教师收藏
    """
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for teacher_org in fav_teachers:
            teacher_id = teacher_org.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,
        })


class MyMessageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    """
    我的消息
    """
    def get(self, request):
        all_message = UserMessage.objects.filter(Q(user=request.user.id) | Q(user=0))
        for message in all_message:
            message.has_read = True
            message.save()
        return render(request, "usercenter-message.html", {
            "all_message":all_message,
        })


class IndexView(View):
    """
    我的消息
    """
    def get(self, request):
        """
        首页展示数据
        """
        courses = Course.objects.all()[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        banners = Banner.objects.all().order_by("index")[:5]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, "index.html", {
            "courses":courses,
            "banner_courses":banner_courses,
            "banners":banners,
            "course_orgs":course_orgs,
        })


def page_not_found(request):
    #全局404页面
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_refuse(request):
    #全局403页面
    from django.shortcuts import render_to_response
    response = render_to_response('403.html', {})
    response.status_code = 403
    return response


def server_problem(request):
    #全局500页面
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
                # Create your views here.
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username","")
#         pass_word = request.POST.get("password","")
#         user = authenticate(username=user_name,password=pass_word)
#         if user is not None:
#             login(request,user)
#             return render(request,"index.html")
#         else:
#             return render(request, "login.html", {"msg":"用户名或密码错误"})
#     elif request.method == "GET":
#         return render(request, "login.html", {})