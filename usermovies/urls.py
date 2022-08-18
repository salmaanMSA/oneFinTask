from django.urls import path
from usermovies import views

urlpatterns = [
    path('register/', views.CreateUserApiView.as_view()),
]
