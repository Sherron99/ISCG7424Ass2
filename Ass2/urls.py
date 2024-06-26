from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

from .views import get_user_id

#touter是可以帮助我们生成URL路由的路由器
#register 方法用于将视图集（ViewSet）注册到路由器，并生成相应的URL路由配置

router = DefaultRouter() #router（在这里是 DefaultRouter）的主要作用是自动生成标准的 CRUD 操作 URL，并将这些 URL 与相应的视图集（ViewSet）绑定。
#DefaultRouter 会为每个注册的视图集自动生成标准的 CRUD 操作 URL。例如，给定一个 SemesterViewSet，
# DefaultRouter 会生成如下 URL：
# GET /semesters/：列出所有学期
# POST /semesters/：创建一个新的学期
# GET /semesters/{pk}/：检索特定学期的详细信息
# PUT /semesters/{pk}/：更新特定学期
# PATCH /semesters/{pk}/：部分更新特定学期
# DELETE /semesters/{pk}/：删除特定学期
#我们是将特定的一个视图集和与特定的url绑定
#下面的register括号里，分别是（1.在router后继续添加的内容，生成新的url 2.视图集（处理指定url的http请求） 3.别名（可选））
router.register('semesters',viewset=views.SemesterViewSet, basename='semesters')
router.register('courses',viewset=views.CourseViewSet, basename='courses')
router.register('students',viewset=views.StudentViewSet, basename='students')
router.register('lecturers',viewset=views.LecturerViewSet, basename='lecturers')
router.register('classes',viewset=views.ClassViewSet, basename='classes')
router.register('enrollments',viewset=views.StudentEnrollmentViewSet, basename='enrollments')
router.register('users',viewset=views.UserViewSet, basename='users') #给用户增删改查
# router.register('grades',viewset=views.StudentGradeViewSet, basename='grades')

urlpatterns = [
    #url模式，视图，别名（可选）
    path("get_user_id/", get_user_id, name="get_user_id"), #我们在这里又添加了一个获取用户id根据lei的视频
    path('students/batch', views.batch_create_users_and_students, name='batch_create_users_and_students'),
    path('', include(router.urls))
     #这里的 '' 是一个空字符串，表示 URL 路径没有额外的前缀
    #由于前缀是空字符串，因此所有由 router 生成的路径都将直接在根路径下可用
]

#总结：
#DefaultRouter有增删改查这几个功能。于是router，可以变成不同的模式，GET/POST/PUT等等，然而register字眼是可以将url和
# viewset进行绑定。于是生成了不同的url。而这些url都会保存到urlpatterns方便于管理。