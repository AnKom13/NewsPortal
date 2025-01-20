"""
URL configuration for NewsPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path


from news.views import PostAPIViewset, CommentAPIViewset, CategoryAPIViewset
from rest_framework import routers

router = routers.DefaultRouter()

router.get_api_root_view().cls.__name__ = "Api for NewsPortal"
router.get_api_root_view().cls.__doc__ = "Простенькое Api для учебного примера"

router.register(r'post', PostAPIViewset)
router.register(r'comment', CommentAPIViewset)
router.register(r'category', CategoryAPIViewset)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')), # подключаем встроенные эндопинты для работы с локализацией
    path('admin/', admin.site.urls),
    # отключил, т.к. делаю вход через allauth
    #    path('accounts/', include('django.contrib.auth.urls')),
    #    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path('pages/', include('django.contrib.flatpages.urls')),
    #    path('about/', include('django.contrib.flatpages.urls')),
#    path('', include('news.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
