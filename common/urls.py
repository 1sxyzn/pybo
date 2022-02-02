from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    #django.contrib.auth 앱의 로그인뷰 클래스를 사용! 그래서 별도의 views.py 수정이 필요 없음!
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('signup/', views.signup, name='signup'),
]