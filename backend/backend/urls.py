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
from BaseTickets.views import CustomAuthToken,group_and_account,ContactFormView,TransbankTransactionAPIView
from django.conf import settings
from django.conf.urls.static import static
from BaseTickets.api import PublicTiqueView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('BaseTickets.urls')),
    path('login/', views.login),
    re_path('register/', views.register),
    path('api/login/', CustomAuthToken.as_view(), name='login'),
    path('group_and_account/<int:user_id>/', group_and_account, name='group_and_account'),
    path('api/public/tiques/', PublicTiqueView.as_view(), name='public-tiques'),
    path('api/Public/Tiques/<int:pk>/', PublicTiqueView.as_view(), name='public-tique-detail'),
    path('contact/', ContactFormView.as_view(), name='contact_form'),
    path('iniciar-transaccion/', TransbankTransactionAPIView.as_view(), name='iniciar-transaccion'),
    path('usuarios/', views.get_all_usuarios, name='list_all_users'),
    path('recibir-pago/', views.recibir_pago, name='recibir_pago'),


    

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
