from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from Ass2 import serializers
from Ass2.models import Semester, Course, StudentEnrolment, Student, Lecturer,Class
from Ass2.serializers import CourseSerializer, ClassSerializer, StudentEnrollmentSerializer, \
    StudentSerializer, LecturerSerializer, SemesterSerializer, UserSerializer


# Create your views here.
#就是我们将要展示的内容，它的def后的名称就是urls里跳转的名称。

# 视图的交互流程
# 客户端请求（用户交互）：
#
# 用户在网页上进行操作，如查看学生列表、添加新学生等。
# 浏览器发送相应的HTTP请求到服务器。
# 视图处理请求：
#
# URL路由将请求转发给相应的ViewSet。
# ViewSet处理请求，调用适当的方法（如list、create、retrieve、update、destroy）。
# 序列化和反序列化：
#
# 对于GET请求，ViewSet查询数据库，获取模型实例，并使用序列化器将其转换为JSON响应。
# 对于POST、PUT、PATCH请求，ViewSet接收JSON数据，使用序列化器进行反序列化，验证并保存数据到数据库。
# 服务器响应：
#
# ViewSet将处理结果序列化为JSON，并返回给客户端。
# 浏览器接收响应并更新用户界面。

#viewset 是对资源的增删改查（CRUD）操作


#使用 viewsets.ModelViewSet 可以同时处理一个模型的增、删、改、查操作。这是因为 ModelViewSet 包含了 Django REST framework 的所有
#通用视图（RetrieveModelMixin、ListModelMixin、CreateModelMixin、UpdateModelMixin 和 DestroyModelMixin）。


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

    #我们的create是需要有responese的
    def create(self, request, *args, **kwargs):
        serializer = SemesterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors)
        return Response(serializer.data)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class StudentEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = StudentEnrolment.objects.all()
    serializer_class = StudentEnrollmentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#下面是根据lei视频添加
@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
def get_user_id(request):
    user = request.user
    # print(f"User object: {user}")
    # print(f"User ID: {user.id}")
    # print(f"User Username: {user.username}")
    serializer = UserSerializer(instance=user)
    return Response(serializer.data)