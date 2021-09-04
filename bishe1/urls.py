"""bishe1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from bishe1 import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("login/",views.login,name='login'),
    path("admin/",admin.site.urls),
    path("myspace/",views.index),
    path("rating/",views.rating),
    path("register/",views.register,name='register'),
    path("list/<int:pindex>", views.index1),
    path("logout/",views.logout),
    path("detail/<title_douban>",views.index3),
    path("movie/",views.movie),
    path("<genres1>/<pindex>",views.index2),
    path("recommend/",views.recommend),
    #path("",views.pinjie)
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
