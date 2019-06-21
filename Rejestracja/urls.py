"""Rejestracja URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from remote_registration.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('remote_registration.urls')),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^user/details/$', UserDetailView.as_view(), name='user_details'),
    url(r'^user/add/$', AddUserView.as_view(), name='user_add'),
    url(r'^user/update/$', UpdateUserView.as_view(), name='user_update'),
    url(r'^user/update/password/$', ChangePasswordView.as_view(), name='user_update_password'),
    url(r'^user/reset/password/$', auth_views.PasswordResetView.as_view(template_name='remote_registration/reset_password.html',
                                                                        success_url=reverse_lazy('user_reset_password_done')),
                                                                        name='user_reset_password'),
    url(r'^user/reset/password/done/$', auth_views.PasswordResetDoneView.as_view(), name='user_reset_password_done'),
    url(r'^user/reset/password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^user/reset/password/complete/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
