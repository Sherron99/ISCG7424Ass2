from django.contrib.auth.models import User
from django.db import models

#反向关系：
#访问反向关系（例如有一个author和一个book，两个class，一个author有零到多本书，一本书有一个author。书class有author的外键。我们可以轻而易举的获取到book的author，但是如果我们要获取到author有哪些book，则需要用到反向关系查询。）
#通过Django自动创建的反向关系管理器，我们可以从 Author 实例中获取所有与之关联的 Book 实例。默认的反向关系管理器名称是 book_set，这是由Django自动生成的。
class Semester(models.Model): #Semester Model
    year = models.IntegerField()
    semester = models.IntegerField()
    courses = models.ManyToManyField('Course', blank=True, null=True)
    #course 和 semester是多对多关系，那么ManyToManyField放在哪一个class里面，取决于哪一个逻辑会更自然或查询更频繁

    def __str__(self):
        return f"{self.year} - Semester {self.semester}"
    #In Django, the __str__ method should return a string representation of the object.
    #这里的def显示的是管理后台显示的内容

class Course(models.Model): #Course Model
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Lecturer(models.Model): #Lecturer Model
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    DOB = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.firstName + self.lastName

class Class(models.Model): #Class Model
    number = models.CharField(max_length=100, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, blank=True, null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='classes_taught') #这里我们有related_name后，我们是可以通过lecturer来获取所有的与他有关的class。related_name指定反向关系的名称
    students = models.ManyToManyField('Student', through='StudentEnrolment')#through指定关系的表名

    def __str__(self):
        return self.number + self.course.name #返回的结果就是 luoluo， 但是如果我们使用return f"{self.number} - {self.course.name}"，就会返回 luoluo - Computer Science.我们这样的话就可以在里面自定义展示内容

class Student(models.Model): #Student Model
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    DOB = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.firstName + self.email


class StudentEnrolment(models.Model): #Student Enrolment Model
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE,related_name="getAllStudentEnrolments")
    grade = models.IntegerField(blank=True, null=True)
    enrolTime = models.DateTimeField(auto_now_add=True) #auto_now_add=True 在创建的时候自动添加
    gradeTime = models.DateTimeField(auto_now=True,blank=True, null=True) #auto_now=True 在修改的时候自动修改