from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^candidate/user/(?P<user_id>[\d]+)/$', views.candidate_profile_page, name='candidate'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^home/$', views.home, name='home'),
    url(r'^profile/user/(?P<user_id>[\d]+)/$', views.user_profile, name='profile'),
    url(r'^post/(?P<post_id>[\d]+)/$', views.view_post, name='view_post'),
    url(r'^create_comment/$', views.create_comment, name='create_comment'),
    url(r'^create_post_page/$', views.create_post_page, name='create_post_page'),
    url(r'^create_post/$', views.create_post, name='create_post'),
    url(r'^delete_post/$', views.delete_post, name='delete_post'),
    url(r'^delete_comment/$', views.delete_comment, name='delete_comment'),
    # API
    url(r'^api/post/(?P<post_id>[\d]+)/$', views.api_post_get, name='view_post'),
    #url(r'^api/post/(?P<post_id>[\d]+)/delete$', views.api_post_delete, name='delet_post'),
    url(r'^api/candidate/(?P<user_id>[\d]+)/$', views.api_candidate_show, name='profile'),
]
