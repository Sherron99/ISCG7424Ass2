from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from Ass2.models import Class, Semester, Lecturer, Student, Course, StudentEnrolment


def create_user_roles():
    groups = ["Administrator", "Lecturer", "Student"]
    for group in groups:
        Group.objects.get_or_create(name=group)


# 调用函数以创建用户组
create_user_roles()
# 自定义用户管理页面
# class CustomUserAdmin(UserAdmin):
#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#
#         # 获取用户所选择的组
#         groups = request.POST.getlist('groups')
#
#         if change:  # 编辑用户时
#             if 'Lecturer' in groups:
#                 if not Lecturer.objects.filter(user=obj).exists():
#                     Lecturer.objects.create(user=obj, firstName=obj.username, lastName='')
#             else:
#                 Lecturer.objects.filter(user=obj).delete()
#
#             if 'Student' in groups:
#                 if not Student.objects.filter(user=obj).exists():
#                     Student.objects.create(user=obj, firstName=obj.username, lastName='')
#             else:
#                 Student.objects.filter(user=obj).delete()
#         else:  # 新建用户时
#             if 'Lecturer' in groups:
#                 Lecturer.objects.create(user=obj, firstName=obj.username, lastName='')
#             if 'Student' in groups:
#                 Student.objects.create(user=obj, firstName=obj.username, lastName='')
#
# admin.site.unregister(User)  # 如果我们想要用自定义的注册模型，必须要先取消注册默认的用户管理，以便可以自定义用户管理。
# admin.site.register(User, CustomUserAdmin)  # 使用自定义的 UserAdmin 类重新注册用户管理。

# Register your models here.
# 允许管理用户对模型进行增删改查，所以这一步里需要包含models里所有的class
admin.site.register(Class)
admin.site.register(Semester)
admin.site.register(Lecturer)
admin.site.register(Student)
admin.site.register(StudentEnrolment)
admin.site.register(Course)
