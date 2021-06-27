"""jsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# include方法，即路由转发，可调用app下的二级urls.py的urlpatterns；static方法自动根据settings下MEDIA_URL和MEDIA_ROOT的配置进行路由模式的设置
# include中的namespace（实例命名空间）主要用于同一个项目不同权限的操作
urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('goto1/', include('polls.urls', namespace='polls_goto1')),
    path('goto2/', include('polls.urls', namespace='polls_goto2'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URLconfs具有一个钩子（hook），允许你传递一个Python字典作为额外的关键字参数给视图函数，像下面这样：
# urlpatterns = [
#     path('blog/<int:year>/', views.year_archive, {'foo': 'bar'}),
# ]
