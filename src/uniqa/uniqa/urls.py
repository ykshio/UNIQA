"""
URL configuration for uniqa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import RedirectView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    # ログイン済みの場合、質問リストへリダイレクト
    if request.user.is_authenticated:
        return redirect('questions:question_list')
    # 未ログインの場合は説明ページを表示
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('questions/', include('questions.urls')),
    path('polls/', include('polls.urls')),
    path('likes/', include('likes.urls')),
    path('', home, name='home'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)