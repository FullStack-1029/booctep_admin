from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
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

    if search == None:
        search = ''
    if page == '' or page == None:
        page = 1
    else:
        page = int(page)
    if type == '' or type == None:
        type = 1
    else :
        type = int(type)
    courses_list = []
    awaiting_count = len(Courses.objects.filter(approval_status=1).filter(Q(name__contains=search) | Q(user_name__contains=search)))
    approved_count = len(Courses.objects.filter(approval_status=2).filter(Q(name__contains=search) | Q(user_name__contains=search)))
    canceled_count = len(Courses.objects.filter(approval_status=3).filter(Q(name__contains=search) | Q(user_name__contains=search)))
    if type*1 == 1:
        courses_list = Courses.objects.filter(approval_status=1).filter(Q(name__contains=search) | Q(user_name__contains=search))
    elif type*1 == 2:
        courses_list = Courses.objects.filter(approval_status=2).filter(Q(name__contains=search) | Q(user_name__contains=search))
    else:
        courses_list = Courses.objects.filter(approval_status=3).filter(Q(name__contains=search) | Q(user_name__contains=search))
    paginator = Paginator(courses_list, 2)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    for course in courses:
        secIdList = Sections.objects.filter(course_id=course.id).values_list('id',flat=True)
        secIdList = map(str, secIdList)
        secIdStr = ','.join(secIdList)
        videoList = VideoUploads.objects.extra(where=['FIND_IN_SET(section_id, "' + secIdStr + '")']).values_list('url',flat=True)
        videoList = map(str, videoList)
        videoUrlStr = ','.join(videoList)
        course.video_url = videoUrlStr

    return render(request, 'review.html', {
        'courses': courses,
        'type': type,
        'search': search,
        'page': page,
        'awaiting_count': awaiting_count,
        'approved_count': approved_count,
        'canceled_count': canceled_count
    })

def test(request):
    search = request.POST.get('search')
    page = request.POST.get('page')
    if search == None:
        search = ''
    video_list = TestVideo.objects.all()
    videoList = []
    for video in video_list:
        user = User.objects.filter(id=video.user_id).filter(Q(email__contains=search) | Q(first_name__contains=search) | Q(last_name__contains=search))
        if len(user) == 1:
            videoList.append(video)

    if page == '' or page == None:
        page = 1
    else :
        page = int(page)
    paginator = Paginator(videoList, 2)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'test.html', {'video_list': videos, 'search': search})

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
    # try:
    #     course_id = request.POST.get('course_id')
    #     course = Courses.objects.get(pk=course_id)
    #     html = render_to_string('mail/course_mail.html', {'course': course})
    #     print("html test:::\n", html)
    #     send_mail('','','',['ernestpapyan96@gmail.com'],fail_silently=False,html_message=html)
    # except:
    #     exit()

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

