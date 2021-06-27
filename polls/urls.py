from django.urls import path
from . import views

# 在项目本身的urls.py中定义命名空间
app_name = 'polls'

# 路由简单的来说就是根据用户请求的 URL 链接来判断对应的处理程序，并返回处理结果，也就是 URL 与 Django 的视图建立映射关系
# name参数用于设置url的别名，在视图函数和模板中可用polls:detail寻找到对应的url，实现反向解析URL、反向URL匹配、反向URL查询或者简单的URL反查
# urlpatterns = [
#     path('', views.index, name='index'),
#     path('<int:question_id>/', views.detail, name='detail'),
#     path('<int:question_id>/results/', views.results, name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote')
# ]

# 可以直接通过http://127.0.0.1:8000/static/polls/images/bg.jpg访问背景图片，而不需要单独配置url
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('polls/', views.goto, name='goto'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('test/', views.test_base, name='test'),
    path('test2/', views.test, name='test2')
]
