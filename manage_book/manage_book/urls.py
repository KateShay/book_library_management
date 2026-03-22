from django.contrib import admin
from django.urls import path
from web_library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('create/', views.create_book, name='create_book'),
    path('edit/<int:id>/', views.edit_book, name='edit_book'),
    path('delete/<int:id>/', views.delete_book, name='delete_book'),
    path('request/<int:id>/', views.request_book, name='request_book'),
    path('cancel_request/<int:id>/', views.cancel_request, name='cancel_request'),
    path('process_request/<int:id>/<str:action>/', views.process_request, name='process_request'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]