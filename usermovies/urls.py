from django.urls import path
from usermovies import views

urlpatterns = [
    path('register/', views.CreateUserApiView.as_view()),
    path('movies/', views.movies_list),
    path('collection/', views.CollectionCreateApiView.as_view())
]
