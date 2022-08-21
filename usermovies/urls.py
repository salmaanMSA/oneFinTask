from django.urls import path
from usermovies import views

urlpatterns = [
    path('register/', views.CreateUserApiView.as_view(), name="register_user"),
    path('movies/', views.movies_list, name="movie_list"),
    path('collection/', views.CollectionApiView.as_view(), name="collec_lst_crt"),
    path('collection/<uuid>/', views.CollectionApiView.as_view(), name="collec_ret_upd_del"),
    path('request-count/', views.get_request_count, name="req_cnt"),
    path('request-count/reset/', views.reset_request_count, name="reset_req_cnt")
]
