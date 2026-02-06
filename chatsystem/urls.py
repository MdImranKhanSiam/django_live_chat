from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register_user, name='registration'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
    path('all_users/', views.all_users, name='all-users'),
    path('all_groups/', views.all_groups, name='all-groups'),
    path('private_chat/<int:pk>', views.private_chat, name='private-chat'),
]
