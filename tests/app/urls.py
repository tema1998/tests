from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('signup', views.Signup.as_view(), name='signup'),
    path('signin', views.Signin.as_view(), name='signin'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('sets', views.Setsview.as_view(), name='sets'),
    path('sets/<int:id>', views.Setview.as_view(), name='set'),
    path('success_signin', views.Success_signin.as_view(), name='success_signin'),
]
