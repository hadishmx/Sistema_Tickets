"""
URL configuration for backend project.

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
from django.urls import path,include, re_path
from BaseTickets import views
from BaseTickets.views import CustomAuthToken,group_and_account
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('BaseTickets.urls')),
    path('login/', views.login),
    re_path('register/', views.register),
    path('api/login/', CustomAuthToken.as_view(), name='login'),
    path('group_and_account/<int:user_id>/', group_and_account, name='group_and_account'),
    

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
