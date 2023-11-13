from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('users/', views.UsersListAPIView.as_view()),
    path('users/<int:pk>/', views.UserRetrieveAPIView.as_view()),

    path("<str:room_name>/", views.room, name="room"),
]
