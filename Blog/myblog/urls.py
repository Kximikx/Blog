from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'), 
    path('post/<int:pk>/', views.post_detail, name='post_detail'), 
    path('post/new/', views.post_new, name='post_new'),  
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),

    path('login/', auth_views.LoginView.as_view(template_name='myblog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'), 

    path('my_posts/', views.my_posts, name='my_posts'),  
    path('profile/', views.profile, name='profile'),     
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
