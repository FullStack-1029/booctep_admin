from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from home.models import *
from teacher.models import *
from django.db.models import Q
import json


# Create your views here.
def login(request):
    return render(request, 'auth/login.html')

def forgetPassword(request):
    return render(request, 'auth/forget-password.html')

def settings(request):
    return render(request, 'settings.html')

def financial(request):
    return render(request, 'financial.html')

def sales(request):
    return render(request, 'sales.html')

def performance(request):
    return render(request, 'performance.html')

def marketing(request):
    return render(request, 'marketing.html')

def security(request):
    return render(request, 'security.html')

def notifications(request):
    return render(request, 'notifications.html')

def expenses(request):
    return render(request, 'expenses.html')

def control(request):
    return render(request, 'control.html')

def works(request):
    return render(request, 'works.html')

def tasks(request):
    return render(request, 'tasks.html')

def discount(request):
    return render(request, 'discount.html')

def refund(request):
    return render(request, 'refund.html')

def spam(request):
    return render(request, 'spam.html')

def courses(request):
    return render(request, 'courses.html')

def review(request):
    search = request.POST.get('search')
    page = request.POST.get('page')
    type = request.POST.get('type')

    print("request::", page, "=====", type)
    if page == '' or page == None:
        page = 1
    else:
        page = int(page)
    if type == '' or type == None:
        type = 1
    else :
        type = int(type)
    courses_list = []
    if type*1 == 1:
        courses_list = Courses.objects.filter(~Q(approval_status=0))
    elif type*1 == 2:
        courses_list = Courses.objects.filter(approval_status=1)
    elif type*1 == 3:
        courses_list = Courses.objects.filter(approval_status=2)
    else:
        courses_list = Courses.objects.filter(approval_status=3)

    paginator = Paginator(courses_list, 20)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    # return render(request, 'review.html', {'all_courses':all_courses, 'waiting_courses': waiting_courses, 'approved_courses':approved_courses, 'canceled_courses':canceled_courses})
    return render(request, 'review.html', {
        'courses': courses,
        'type': type,
        'search': search,
        'page': page
    })

def test(request):
    search = request.POST.get('search')
    page = request.POST.get('page')
    video_list = TestVideo.objects.all()
    if page == '' or page == None:
        page = 1
    else :
        page = int(page)
    paginator = Paginator(video_list, 7)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'test.html', {'video_list': videos})

def teachers(request):
    return render(request, 'teachers.html')

def students(request):
    return render(request, 'students.html')

def employees(request):
    return render(request, 'employees.html')

def superusers(request):
    return render(request, 'superusers.html')


#handling api request...
@csrf_exempt
def getCourseById(request):
    course_id = request.POST.get('course_id')
    print("course_id", course_id)
    course = Courses.objects.get(pk=course_id)
    # course.username = course.user.first_name + ' ' + course.user.last_name
    user = User.objects.get(pk=course.user_id)
    course_list = serializers.serialize('json', [course])
    ret = {
        'name': user.first_name + ' ' + user.last_name,
        'course': course_list
    }
    return JsonResponse(ret, safe=False)

@csrf_exempt
def getTestVideoById(request):
    id = request.POST.get('id')
    user_id = request.POST.get('user_id')
    video = TestVideo.objects.get(pk=id)
    user = User.objects.get(pk=user_id)
    ret = {
        'user': serializers.serialize('json', [user]),
        'video': serializers.serialize('json', [video])
    }
    return JsonResponse(ret, safe=False)

@csrf_exempt
def deleteVideoById(request):
    id = request.POST.get('id')
    TestVideo.objects.get(pk=id).delete()
    ret = {
        'msg': 'success'
    }
    return JsonResponse(ret)

@csrf_exempt
def setApprove(request):
    course_id = request.POST.get('course_id')
    course = Courses.objects.get(pk=course_id)
    course.approval_status = 2
    course.save()
    ret = {
        'msg': 'success'
    }
    return JsonResponse(ret)

@csrf_exempt
def setCancel(request):
    course_id = request.POST.get('course_id')
    course = Courses.objects.get(pk=course_id)
    course.approval_status = 3
    course.save()
    ret = {
        'msg': 'success'
    }
    return JsonResponse(ret)

