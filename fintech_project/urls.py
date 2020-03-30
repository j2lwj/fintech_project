"""fintech_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from portfolio import views
from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views

# Albert - https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html
"""
https://simpleisbetterthancomplex.com/references/2016/10/10/url-patterns.html

Primary Key Autofield: url(r'^questions/(?P<pk>\d+)/$', views.question_details, name='question_details'),
Slug/String Fields: url(r'^posts/(?P<slug>[-\w]+)/$', views.post, name='post'),
Slug with Primary Key: url(r'^blog/(?P<slug>[-\w]+)-(?P<pk>\d+)/$', views.blog_post, name='blog_post'),
Usernames: url(r'^profile/(?P<username>[\w.@+-]+)/$', views.user_profile),
Year: url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
Year/Months: url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
Year/Months/Days: url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.article_detail)
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('compare/', views.compare, name='compare'),
    path('my_portfolio/', views.my_portfolio, name='my_portfolio'),
    path('portfolios/', views.portfolios, name='portfolios'),
    re_path(r'^/portfolios/(?P<id>\d+)/$', views.portfolio_id, name='portfolio_id'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', views.signup, name='signup')
]
