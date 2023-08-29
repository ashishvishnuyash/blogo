from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('login', views.auth_login),
    path('signup', views.signup),
    path('logout', views.authlogout),
    path('postblog', views.postblog),
    path('blogsubmit', views.blogsubmit),
    path('submitcomment', views.submit_comment),
] 
