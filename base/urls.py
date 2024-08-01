from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/<str:st>/', views.profile, name='profile'),
    path('adding/<str:id>/', views.adding, name='adding'),
    path('delete/<str:id>/', views.delete, name='delete'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),
    path('add/', views.add_mark, name='add'),
    path('view/<str:id>/', views.view, name='view'),
    path('delete_mark/<str:id>', views.delete_mark, name='delete_mark'),
    path('update_user/', views.update_user, name='update_user')
]
