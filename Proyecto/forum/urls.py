from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main , name='forum'),
    path('create_post/', views.create_post, name='create_post'),
    path('/<str:category>/', views.filter_by_category, name='filter_by_category'),  # New route
    path('mis_publicaciones/', views.mis_publicaciones, name='mis_publicaciones'),
    path('admin_approval/', views.admin_approval, name='admin_approval'),
    path('accept_post/<int:post_id>/', views.accept_post, name='accept_post'),
    path('reject_post/<int:post_id>/', views.reject_post, name='reject_post'),
]