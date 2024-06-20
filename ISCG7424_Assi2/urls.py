"""
URL configuration for ISCG7424_Assi2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Ass2/', include('Ass2.urls')), #这一步得在migration后使用
    path('auth/',obtain_auth_token) #这里的obtain_auth_token十分重要，它相当于是用户是否登陆成功，是否有账号。如果账号和密码都正确，就会给我们发送一个token。
    #用户在输入账号和密码后，django会在user类里面进行筛查，验证这个账号和密码。成功则给我们发送token。
    #使用 Token 是为了实现无状态的用户认证。Token 是一种认证机制，常用于 RESTful API 中。通过 Token，可以确保每个请求都带有用户的身份信息，从而不需要在每个请求中重新进行用户名和密码的认证。
]
