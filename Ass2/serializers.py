from django.contrib.auth.models import User
from rest_framework import serializers

from Ass2.models import Course, Semester, Lecturer, Student, Class, StudentEnrolment

#序列化输出 反序列化输入
#序列化（Serialization） 是指将复杂的数据类型（如Django模型实例）转换为Python原生数据类型，然后再转换为JSON或XML等格式，以便通过网络传输或在客户端展示。

#反序列化（Deserialization） 是指将从客户端接收到的数据（通常是JSON或XML格式）转换为Python原生数据类型，然后再转换为Django模型实例，以便在服务器端进行处理和存储。


#我们可以通过使用write_only=True 和 read_only=True来控制什么时候显示。
#注意：1.嵌套关系的使用（尤其是model里的多对多，一对多，一对一））
#2.如果有时用到serializers.StringRelatedField()，那么它等于model里该class的__str__方法，return的是什么，显示的就是什么

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'name']

# class simpleCourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = ['code', 'name']

class SemesterSerializer(serializers.ModelSerializer):
     courses = CourseSerializer(many=True)  # 我们使用many = True，则会返回一个数组
     class Meta:
         model = Semester
         fields = ['id', 'year', 'semester', 'courses']

# class simpleSemesterSerializer(serializers.ModelSerializer):
#     courses = CourseSerializer(many=True)
#     class Meta:
#         model = Semester
#         exclude = ['id']
#注意：1.如果我需要SemesterSerializer中的courses只显示部分CourseSerializer里的field的话，我有两种方法，要不然就是创建一个新的(simpleSemesterSerializer)，要不然就是修改原有的CourseSerializer，要不然就是使用exclude


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['id', 'firstName', 'lastName', 'email', 'DOB', 'user']

#对于LecturerSerializer和StudentSerializer都遇到了一个问题，user是否要写到这个fields里面

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'firstName', 'lastName', 'email', 'DOB', 'user']

class ClassSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    semester = SemesterSerializer()
    students = StudentSerializer(many=True)
    lecturer = LecturerSerializer()
    class Meta:
        model = Class
        fields = ['id', 'number', 'course', 'semester', 'lecturer', 'students']

class StudentEnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    Class = ClassSerializer()
    enrolTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    gradeTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = StudentEnrolment
        fields = ['id', 'student', 'Class', 'grade', 'enrolTime', 'gradeTime']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True, 'required': True}} #extra key word argument是被用来设置password的额外参数.
#write_only表示只接受反序列化输入时也就是创建时显示，反之，序列化输出的时候时不可见的。
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password']) #set_password 方法会对密码进行哈希处理，而不是直接存储原始密码，以确保安全性。
        user.save()
        return user