import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import authentication, permissions

from . import models
from . import serializers

User = get_user_model()


def index(request):
    return render(request, "chat/index.html")


@login_required
def room(request, room_name):
    return render(request, "chat/room.html", {
        "room_name_json": mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })


class UsersListAPIView(generics.ListAPIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    View to show one user in the system.

    * Requires token authentication.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
