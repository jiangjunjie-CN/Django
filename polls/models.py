from django.db import models
import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
# Create your models here.



"""
 该类是用来生成数据库的 必须要继承models.Model
"""
# class Student(models.Model):
#     """
#     创建如下几个表的字段
#     """
#     # 学号 primary_key=True: 该字段为主键
#     studentNum = models.CharField('学号', primary_key=True, max_length=15)
#     # 姓名 字符串 最大长度20
#     name = models.CharField('姓名', max_length=20)
#     # 年龄 整数 null=False, 表示该字段不能为空
#     age = models.IntegerField('年龄', null=False)
#     # 性别 布尔类型 默认True: 男生 False:女生
#     sex = models.BooleanField('性别', default=True)
#     # 手机 unique=True 该字段唯一
#     mobile = models.CharField('手机', unique=True, max_length=15)
#     # 创建时间 auto_now_add：只有在新增的时候才会生效
#     createTime = models.DateTimeField(auto_now_add=True)
#     # 修改时间 auto_now： 添加和修改都会改变时间
#     modifyTime = models.DateTimeField(auto_now=True)
#
#     # 指定表名 不指定默认APP名字——类名(app_demo_Student)
#     class Meta:
#         db_table = 'student'
#
#
# """
# 学生社团信息表
# """
# class studentUnion(models.Model):
#     # 自增主键, 这里不能设置default属性，负责执行save的时候就不会新增而是修改元素
#     id = models.IntegerField(primary_key=True)
#     # 社团名称
#     unionName = models.CharField('社团名称', max_length=20)
#     # 社团人数
#     unionNum = models.IntegerField('人数', default=0)
#     # 社团负责人 关联Student的主键 即studentNum学号 一对一的关系,on__delete 属性在django2.0之后为必填属性后面会介绍
#     unionRoot = models.OneToOneField(Student, on_delete=None)
#
#     class Meta:
#         db_table = 'student_union'
#

"""
OneToOneField： 一对一
ForeignKey: 一对多
ManyToManyField： 多对多(没有ondelete 属性)
"""

def user_directory_path(instance, filename):
    # 文件上传到MEDIA_ROOT/user_<id>/<filename>目录中
    return 'question_{}/{}'.format(instance.question.id, filename)

# 测试用的模型验证器
def validate_imgFormat(value):
    if value.split('.')[1] not in ['png', 'jpg', 'jpeg']:
        raise ValidationError(
            _('%(value)s is not a image file'),
            params={'value': value},
        )


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    # 如果你有一段需要针对每个模型实例都有效的业务代码，应该把它们抽象成为一个函数，放到模型中成为模型方法，而不是在大量视图中重复编写这段代码，或者在视图中抽象成一个函数
    def was_publish_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    # 提供一些属性来改进admin页面输出的样式
    was_publish_recently.admin_order_field = 'pub_date'
    was_publish_recently.boolean = True
    was_publish_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # ManyToManyField，多对多
    # question = models.ManyToManyField('Question')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    # 设置模型的元数据（非必须），例如数据排序，表格名（默认为app名_模型名），反向关联名（默认为源模型的名字_set）
    class Meta:
        # 通过查询语句，获得Queryset后的列表内元素的顺序，如果在字段名前加上字符“-”则表示按降序排列，如果使用字符问号“？”表示随机排列
        ordering = ['-votes']
        verbose_name_plural = 'oxen'
        # 联合唯一，一旦二者都相同，则会被Django拒绝创建，并且强制应用于数据库层面
        # 接收一个二维的列表，每个元素都是一维列表，表示一组联合唯一约束
        unique_together = [['question', 'choice_text'], ]
        # 联合索引，用法和特性类似unique_together
        index_together = [['question', 'choice_text'], ]

    def __str__(self):
        return self.choice_text

    def vote_level(self):
        if self.votes >= 5:
            return 'high'
        else:
            return 'low'

# user_directory_path这种回调函数，必须接收两个参数，然后返回一个Unix风格的路径字符串。参数instace代表一个定义了FileField的模型的实例，说白了就是当前数据记录。filename是原本的文件名。


class Test(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # 模型建立ImageField或FileField前，需要在setting中配置本地上传路径和url路径,upload_to也可以进行简单的字符串配置，例如'uploads/%Y/%m/%d/'
    # null 是针对数据库而言，如果 null = True, 表示数据库的该字段可以为空；blank 是针对表单的，如果 blank = True，表示你的表单填写该字段的时候可以不填，但是对数据库来说，没有任何影响
    # height_field 和 width_field，分别保存图片的高度和宽度信息
    img = models.ImageField('图片', upload_to=user_directory_path, blank=True, null=True, height_field=None, width_field=None, validators=[validate_imgFormat])

    # 这里定义一个方法，作用是当用户注册时没有上传照片，模板中调用 [ModelName].[ImageFieldName].url 时赋予一个默认路径
    # def photo_url(self):
    #     if self.photo and hasattr(self.photo, 'url'):
    #         return self.photo.url
    #     else:
    #         return '/media/default/user.jpg'

class Comment(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()
    # 使用self创建递归外键，即自己关联自己的外键，典型的例子是评论系统
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)


# class Student(models.Model):
#     FRESHMAN = 'FR'
#     SOPHOMORE = 'SO'
#     JUNIOR = 'JR'
#     SENIOR = 'SR'
#     YEAR_IN_SCHOOL_CHOICES = (
#         (FRESHMAN, 'Freshman'),
#         (SOPHOMORE, 'Sophomore'),
#         (JUNIOR, 'Junior'),
#         (SENIOR, 'Senior'),
#     )
# 用于页面上的选择框标签，需要先提供一个二维的二元元组，第一个元素表示存在数据库内真实的值，第二个表示页面上显示的具体内容。在浏览器页面上将显示第二个元素的值
# 模型实例的get_year_in_school_display()方法可以获取第二个元素
#     year_in_school = models.CharField(
#         max_length=2,
#         choices=YEAR_IN_SCHOOL_CHOICES,
#         default=FRESHMAN,
#     )
#
#     def is_upperclass(self):
#         return self.year_in_school in (self.JUNIOR, self.SENIOR)