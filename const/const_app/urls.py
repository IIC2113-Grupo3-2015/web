from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^candidate/user/(?P<user_id>[\d]+)/$', views.candidate_profile_page, name='candidate'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/user/(?P<user_id>[\d]+)/$', views.user_profile, name='profile'),
    url(r'^post/(?P<post_id>[\d]+)/$', views.view_post, name='view_post'),
    url(r'^create_comment/$', views.create_comment, name='create_comment'),
    url(r'^create_post_page/$', views.create_post_page, name='create_post_page'),
    url(r'^create_post/$', views.create_post, name='create_post'),
]
