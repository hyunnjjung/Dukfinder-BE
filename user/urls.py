"""
URL configuration for finalPrj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from .views import RegisterView, LoginView, ProfileView, UserinfoView, PasswordView, MyLostListView, MyFindListView, BulkDeleteView, UpdateFoundStatusBulkView

app_name = 'user'

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/<int:pk>/', ProfileView.as_view()),
    path('userinfo/', UserinfoView.as_view()),
    path('password/', PasswordView.as_view()),

    path('mylost/', MyLostListView.as_view()), # 마이페이지에서 보일
    path('myfind/', MyFindListView.as_view()),
    path('bulk-delete/<str:lost_ids>/<str:find_ids>/', BulkDeleteView.as_view(), name='bulk-delete'),
    path('mypost/bulk-update/<str:pk_ids>/', UpdateFoundStatusBulkView.as_view(), name='my-post-bulk-update'),
]

