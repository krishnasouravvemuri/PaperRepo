from django.urls import path
import auther.views as v

urlpatterns = [
    path('' , v.home , name = "home"),
    path('signup/' , v.signup_view , name = "signup"),
    path('login/' , v.login_view , name = "login"),
    path('logout/' , v.logout_user , name = "logout" )
]