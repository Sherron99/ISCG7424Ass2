from django.contrib.auth.models import User, Group
from rest_framework import serializers

from Ass2.models import Course, Semester, Lecturer, Student, Class, StudentEnrolment


# 序列化输出 反序列化输入
# 序列化（Serialization） 是指将复杂的数据类型（如Django模型实例）转换为Python原生数据类型，然后再转换为JSON或XML等格式，以便通过网络传输或在客户端展示。

# 反序列化（Deserialization） 是指将从客户端接收到的数据（通常是JSON或XML格式）转换为Python原生数据类型，然后再转换为Django模型实例，以便在服务器端进行处理和存储。


# 我们可以通过使用write_only=True 和 read_only=True来控制什么时候显示。
# 注意：1.嵌套关系的使用（尤其是model里的多对多，一对多，一对一））
# 2.如果有时用到serializers.StringRelatedField()，那么它等于model里该class的__str__方法，return的是什么，显示的就是什么

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'name']


#Semester遇到的问题是，我们在postman不能创建新的semester，因为有course这个嵌套文字。
#我们只希望用户在创建semester的时候，能够从course里添加现有的course，而不是直接创建新的course。
class SemesterCreateSerializer(serializers.ModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True) #我这里设置了many = True，就是可以传入多个course
    #这里的PrimaryKeyRelatedField它允许你在序列化器中通过主键字段来引用相关对象

    class Meta:
        model = Semester
        fields = ['id', 'year', 'semester', 'courses']

#create函数里（self表示当前的serializer实例。它允许我们访问序列化器的属性和方法。）validated_data 是用户在界面输入的值，通过序列化器验证后得到的一个字典。这个字典包含了所有经过验证的字段和值。
#下面这里的create和update都是对应着postman的put，patch，post

    def create(self, validated_data):
        year = validated_data.pop('year')
        semester = validated_data.pop('semester')
        courses_data = validated_data.pop('courses')#pop既可以表示移除也可以表示提取。所以这一行代码进行了两个步骤：1.将validated_data中的数据里移除courses。2.courses_data则包含了courses
        if Semester.objects.filter(year=year, semester=semester).exists():
            raise serializers.ValidationError("Semester with the same year and semester already exists.")
        semester = Semester.objects.create(year=year, semester=semester)
        semester.courses.set(courses_data)#敲重点！！！对于多对多的关系，我们需要手动去处理他们之间的关系，也就是需要用到set。pop这些！！！
        return semester

#instance表示当前正在更新的semester实例
    def update(self, instance, validated_data):
        courses_data = validated_data.pop('courses')

        instance.year = validated_data.get('year', instance.year)
        instance.semester = validated_data.get('semester', instance.semester)
        instance.save()

        instance.courses.set(courses_data)
        return instance

class SemesterReadSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True)  # 读取时返回课程详细信息

    class Meta:
        model = Semester
        fields = ['id', 'year', 'semester', 'courses']

# class simpleSemesterSerializer(serializers.ModelSerializer):
#     courses = CourseSerializer(many=True)
#     class Meta:
#         model = Semester
#         exclude = ['id']
# 注意：1.如果我需要SemesterSerializer中的courses只显示部分CourseSerializer里的field的话，我有两种方法，要不然就是创建一个新的(simpleSemesterSerializer)，要不然就是修改原有的CourseSerializer，要不然就是使用exclude


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['id', 'firstName', 'lastName', 'email', 'DOB', 'user']

    # def create(self, validated_data):
    #     email = validated_data.pop('email')
    #     first_name = validated_data.pop('firstName', '')
    #     last_name = validated_data.pop('lastName', '')
    #     DOB = validated_data.pop('DOB')
    #     if User.objects.filter(email=email).exists():
    #         lecturer = Lecturer.objects.create(email=email, firstName=first_name, lastName=last_name, DOB=DOB)
    #         lecturer.user =
    #         user.save()
    #
    #     return user


# 对于LecturerSerializer和StudentSerializer都遇到了一个问题，user是否要写到这个fields里面

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'firstName', 'lastName', 'email', 'DOB', 'user']


class ClassSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    semester = serializers.PrimaryKeyRelatedField(queryset=Semester.objects.all())
    lecturer = serializers.PrimaryKeyRelatedField(queryset=Lecturer.objects.all())
    students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)

    class Meta:
        model = Class
        fields = ['id', 'number', 'course', 'semester', 'lecturer', 'students']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['course'] = CourseSerializer(instance.course).data
        representation['semester'] = SemesterReadSerializer(instance.semester).data
        representation['lecturer'] = LecturerSerializer(instance.lecturer).data
        representation['students'] = StudentSerializer(instance.students, many=True).data
        return representation

    def create(self, validated_data):
        students_data = validated_data.pop('students')
        class_ = Class.objects.create(**validated_data)
        class_.students.set(students_data)
        return class_

    def update(self, instance, validated_data):
        students_data = validated_data.pop('students')
        instance.number = validated_data.get('number', instance.number)
        instance.course = validated_data.get('course', instance.course)
        instance.semester = validated_data.get('semester', instance.semester)
        instance.lecturer = validated_data.get('lecturer', instance.lecturer)
        instance.save()
        instance.students.set(students_data)
        return instance



class StudentEnrollmentSerializer(serializers.ModelSerializer):
    firstName = serializers.SerializerMethodField()
    lastName = serializers.SerializerMethodField()
    number = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    semester = serializers.SerializerMethodField()
    enrolTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    gradeTime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = StudentEnrolment
        fields = ['id', 'firstName', 'lastName', 'number', 'course', 'semester', 'grade', 'enrolTime', 'gradeTime']

    def get_firstName(self, obj):
        return obj.student.firstName

    def get_lastName(self, obj):
        return obj.student.lastName

    def get_number(self, obj):
        return obj.Class.number

    def get_course(self, obj):
        return {
            "id": obj.Class.course.id,
            "name": obj.Class.course.name
        }

    def get_semester(self, obj):
        return {
            "year": obj.Class.semester.year,
            "semester": obj.Class.semester.semester
        }

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'groups']
        extra_kwargs = {# extra key word argument是被用来设置password的额外参数.
            'password': {'write_only': True, 'required': True}# write_only表示只接受反序列化输入时也就是创建时显示，反之，序列化输出的时候时不可见的。
        }

    def create(self, validated_data):#这里的create对应着postman的post
        groups_data = validated_data.pop('groups', [])#这里的第二个值一样也是可选的，如果当groups不存在，就显示[]
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),#这里的第二个值是可选的，如果当我们获取first_name，如果不存在就显示‘’
            last_name=validated_data.get('last_name', '')
        )

        for group in groups_data:
            user.groups.add(group)

        return user
    # set_password 方法会对密码进行哈希处理，而不是直接存储原始密码，以确保安全性。