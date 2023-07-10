"""infobeans_polling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include,re_path
from infobeans_polling_app import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.indexView.as_view(), name='indexView'),
    path('home/', views.home, name='home'),
    path('infobeans_polling_app/', include('infobeans_polling_app.urls')),
    path('admin/', admin.site.urls),
    path('special/', views.special, name='special'),
    # path('userauth_app/', include('userauth_app.urls')),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('result/<poll_id>/', views.result, name='result'),
    path('vote/<poll_id>/', views.vote, name='vote'),
    path('profile/', views.profile, name='profile'),
    path('posts/', include("posts.urls", namespace="posts")),
    path('groups/', include("groups.urls", namespace="groups")),
    path('blog/', include(('blog.urls', 'blog'), namespace="blog")),
]

# Only add this when we are in debug mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)