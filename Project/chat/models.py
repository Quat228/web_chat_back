from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_20_messages():
        return Message.objects.all().order_by('-timestamp')[:20]


# class Room(models.Model):
#     name = models.CharField(max_length=128, unique=True)
#     is_private = models.BooleanField(default=False)
#
#     def online_users(self):
#         return [user.user_id for user in self.online.all()]
#
#     def get_online_count(self):
#         return self.online.count()
#
#     def join(self, user_id):
#         self.online.create(user_id=user_id)
#         self.save()
#
#     def leave(self, user):
#         self.online.delete(user_id=user.id)
#         self.save()
#
#     def get_last_message(self):
#         messages = Message.objects.filter(room=self).order_by('-timestamp')
#         if messages:
#             return (messages[0].content, messages[0].timestamp.strftime('%d.%m.%Y %H:%M:%S'))
#
#     def __str__(self):
#         return f'{self.name} ({self.get_online_count()})'
#
#
# class RoomUsers(models.Model):
#     room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='online')
#     user_id = models.IntegerField(unique=True)
#     username = models.CharField(max_length=128, null=True, blank=True, unique=True)
#
#     class Meta:
#         unique_together = ('room', 'user_id', 'username')
#
#     def __str__(self):
#         return f'{self.room.name} - {self.user_id}'
#
#
# class Message(models.Model):
#     user = models.IntegerField()
#     room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
#     content = models.CharField(max_length=512)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.user}: {self.content} [{self.timestamp}]'
#
#     def get_username(self):
#         return RoomUsers.objects.get(user_id=self.user).username
