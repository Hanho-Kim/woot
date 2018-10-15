from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
from django.http import HttpResponse
import django.views.defaults

from . import views
from underbar import settings


urlpatterns = [
	url('index', views.index, name='index'),
	url('login', views.login, name='login'),
	url('update', views.update, name='update'),
	url(r'^login/', views.login, name='login'),
	url(r'^notification/', views.notification, name='notification'),
	url(r'^write/', views.write, name='write'),
	url(r'^gathering/', views.gathering, name='gathering'),
	url(r'^people/', views.people, name='people'),
	url(r'^pullup/', views.pullup, name='pullup'),
	url(r'^board/', views.board, name='board'),
	url(r'^footer-input/', views.footerInput, name='footerInput'),
	url(r'^api/v1/', views.apiv1, name='apiv1')
]

urlpatterns += staticfiles_urlpatterns()
