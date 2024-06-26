from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from Ass2 import serializers
from Ass2.models import Semester, Course, StudentEnrolment, Student, Lecturer, Class
from Ass2.permissions import IsAuthorOrReadOnly, IsLecturer, IsStudent
from Ass2.serializers import CourseSerializer, ClassSerializer, StudentEnrollmentSerializer, \
    StudentSerializer, LecturerSerializer, UserSerializer, SemesterReadSerializer, \
    SemesterCreateSerializer


# Create your views here.
# 就是我们将要展示的内容，它的def后的名称就是urls里跳转的名称。

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

# viewset 是对资源的增删改查（CRUD）操作


# 使用 viewsets.ModelViewSet 可以同时处理一个模型的增、删、改、查操作。这是因为 ModelViewSet 包含了 Django REST framework 的所有
# 通用视图（RetrieveModelMixin、ListModelMixin、CreateModelMixin、UpdateModelMixin 和 DestroyModelMixin）。


class SemesterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    queryset = Semester.objects.all()

    # permission_classes = (IsAuthorOrReadOnly,) #你只有是你创建的你才可以update和delete

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:  # list是用于处理get所有实例的请求，retrieve是用于处理get单个实例的请求
            return SemesterReadSerializer
        return SemesterCreateSerializer

    # 我们的create是需要有responese的
    # 这串代码有问题，framework不支持可写的嵌套字段
    # def create(self, request, *args, **kwargs):
    #     serializer = SemesterSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #     else:
    #         return Response(serializer.errors)
    #     return Response(serializer.data)
    #
    # def update(self, request, *args, **kwargs):
    #     serializer = SemesterSerializer(data=request.data)
    #     if serializer.is_valid(): #this one is always required, otherwise you cannot see any errors
    #         super().update(request, *args, **kwargs)
    #         instance = self.get_object()
    #     else:
    #         return Response(serializer.errors)
    #     serializer = SemesterSerializer(instance = instance)
    #     return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # authentication_classes = ([TokenAuthentication, ])
    # permission_classes = [IsAuthenticated, IsAuthor]


class ClassViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class StudentEnrollmentViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = StudentEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            try:
                lecturer = Lecturer.objects.get(user=user)
                # 获取讲师教授的所有班级
                classes = Class.objects.filter(lecturer=lecturer)
                # 返回这些班级中的所有学生注册信息
                return StudentEnrolment.objects.filter(Class__in=classes)
            except Lecturer.DoesNotExist:
                try:
                    student = Student.objects.get(user=user)
                    return StudentEnrolment.objects.filter(student=student)
                except Student.DoesNotExist:
                    return StudentEnrolment.objects.none()
        return StudentEnrolment.objects.none()

    def update(self, request, *args, **kwargs):
        user = request.user
        try:
            lecturer = Lecturer.objects.get(user=user)
            # 只有讲师才能更新成绩
            return super().update(request, *args, **kwargs)
        except Lecturer.DoesNotExist:
            return Response({"detail": "You don't have permission to perform this action."}, status=403)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class LecturerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


# 下面是根据lei视频添加
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_user_id(request):
    user = request.user
    # print(f"User object: {user}")
    # print(f"User ID: {user.id}")
    # print(f"User Username: {user.username}")
    serializer = UserSerializer(instance=user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def User_logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response("User logged out successfully")


@api_view(['POST'])
def batch_create_users_and_students(request):
    if not isinstance(request.data, list):
        return Response({"error": "Expected a list of data"}, status=status.HTTP_400_BAD_REQUEST)

    user_data_list = []
    student_data_list = []

    for item in request.data:
        user_data = {
            'username': item.get('username'),
            'first_name': item.get('first_name'),
            'last_name': item.get('last_name'),
            'email': item.get('email'),
            'password': item.get('password'),  # 确保提供了密码
        }
        user_data_list.append(user_data)

    user_serializer = UserSerializer(data=user_data_list, many=True)
    if user_serializer.is_valid():
        users = user_serializer.save()
        for user in users:
            student_data = {
                'user': user.id,
                'other_student_fields': item.get('other_student_fields'),  # 替换为实际的学生字段
            }
            student_data_list.append(student_data)

        student_serializer = StudentSerializer(data=student_data_list, many=True)
        if student_serializer.is_valid():
            student_serializer.save()
            return Response({"message": "Users and students created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class StudentGradeViewSet(viewsets.ViewSet):
#
#     # permission_classes = [IsAuthenticated, IsStudent]
#     # authentication_classes = (TokenAuthentication,)
#     def list(self, request):
#         user_groups = request.user.groups.values_list('name', flat=True)
#         if 'Student' in user_groups:
#             email = request.user.username
#             student = Student.objects.get(email=email)
#             enrollments = StudentEnrolment.objects.filter(student=student)
#             # enrollments = student.enrollments.all()
#             serializer = StudentEnrollmentSerializer(enrollments, many=True)
#             return Response(serializer.data)
#
#         return Response(status=404)
