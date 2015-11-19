from django.conf.urls import include, url
from django.contrib import admin
from tango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<url>[\w\-]+)/$', views.category, name='category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<url>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^profile/$', views.profile, name='profile'),
]