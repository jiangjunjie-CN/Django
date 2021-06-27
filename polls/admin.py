from django.contrib import admin
from .models import Question, Choice, Test
# Register your models here.

# admin.StackedInline为堆叠式展示，admin.TabularInline为表单式展示
class ChoiceInline(admin.TabularInline):
    '''
    上面的代码相当于告诉Django，Choice对象将在Question管理页面进行编辑，默认情况，请提供3个Choice对象的编辑区域
    '''
    model = Choice
    extra = 3

class TestInline(admin.TabularInline):
    model = Test
    extra = 1

class Questionadmin(admin.ModelAdmin):
    '''
    fields方式进行admin网站中发布时间和问题的展示顺序的修改
    fieldsets方式进行admin网站中发布时间和问题的展示顺序的高级修改
    '''
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']})
    ]
    inlines = [ChoiceInline, TestInline]
    # 页面默认显示model中__str__的部分，list_display可以指定展示的model中的字段以及定义的函数
    list_display = ['question_text', 'pub_date', 'was_publish_recently']
    # 根据你选择的过滤条件的不同，Django会在面板中添加不同的过滤选项
    list_filter = ['pub_date']
    # 可以使用任意多个搜索字段，Django在后台使用的都是SQL查询语句的LIKE语法，但是有限制的搜索字段有助于后台的数据库查询效率
    search_fields = ['question_text']

admin.site.register(Question, Questionadmin)
# admin.site.register(Choice)
