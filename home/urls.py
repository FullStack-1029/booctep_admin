from django.conf.urls import include, url, i18n
from home.views import *

urlpatterns = [

    # get request
    url(r'^$', login, name='login'),
    url(r'^forgetPassword/$', forgetPassword, name='forget password'),
    url(r'^settings/$', settings, name='settings'),
    url(r'^financial/$', financial, name='financial'),
    url(r'^sales/$', sales, name='sales'),
    url(r'^performance/$', performance, name='performance'),
    url(r'^marketing/$', marketing, name='marketing'),
    url(r'^security/$', security, name='security'),
    url(r'^notifications/$', notifications, name='notifications'),
    url(r'^expenses/$', expenses, name='expenses'),
    url(r'^control/$', control, name='control'),
    url(r'^works/$', works, name='works'),
    url(r'^tasks/$', tasks, name='tasks'),
    url(r'^discount/$', discount, name='discount'),
    url(r'^refund/$', refund, name='refund'),
    url(r'^spam/$', spam, name='spam'),
    url(r'^courses/$', courses, name='courses'),
    url(r'^review/$', review, name='review'),
    url(r'^test/$', test, name='test'),
    url(r'^teachers/$', teachers, name='teachers'),
    url(r'^students/$', students, name='students'),
    url(r'^employees/$', employees, name='employees'),
    url(r'^superusers/$', superusers, name='superusers'),

    #add course complete request comes.. add them to page..
    url(r'^getCourseById/$', getCourseById, name='superusers'),
    url(r'^getTestVideoById/$', getTestVideoById, name='superusers'),
    url(r'^setApprove/$', setApprove, name='superusers'),
    url(r'^setCancel/$', setCancel, name='superusers'),
    url(r'^deleteVideoById/$', deleteVideoById, name='superusers'),
]
