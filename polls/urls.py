from django.urls import path
from django.contrib.auth import views as auth_views
from polls import views
# from .views import Home

urlpatterns = [
    
    path('', views.index, name="home"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name="logout"),
    path('register/', views.register, name="register"),
    path('mypolls/',views.mypolls,name='mypolls'),
    path('addpoll/',views.addpoll,name='addpoll'),
    path('about/',views.about,name='about'),


    path('vote/<int:id>/',views.vote, name="vote"),
    path('delete/<id>/',views.delete, name="delete"),
    path('update/<id>/',views.update, name="update"),

    # path('vote/', views.vote, name='vote'),

    # Class based Homepage view
    # path('', Home.as_view(), name="home")
]