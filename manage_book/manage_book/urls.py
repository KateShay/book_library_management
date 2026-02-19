from django.contrib import admin
from django.urls import path
from web_library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path("edit/<int:id>/", views.edit, name="edit"),
    path("delete/<int:id>/", views.delete, name="delete"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
