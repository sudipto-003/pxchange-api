from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q

class ChatManager(models.Manager):
    def get_or_create(self, user1_name, user2_name):
        if user1_name == user2_name:
            return None, False

        q1 = Q(participant1__username=user1_name) & Q(participant2__username=user2_name)
        q2 = Q(participant1__username=user2_name) & Q(participant2__username=user1_name)
        u_chat = self.get_queryset().filter(q1 | q2).distinct()
        if u_chat.exists():
            return u_chat.first(), False
        else:
            try:
                u1 = get_user_model().objects.get(username=user1_name)
                u2 = get_user_model().objects.get(username=user2_name)

                new_chat = self.model(participant1=u1, participant2=u2)
                new_chat.save()

                return new_chat, True
            
            except get_user_model().DoesNotExist:

                return None, False


class Chat(models.Model):
    participant1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='participant1')
    participant2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='participant2')
    since = models.DateTimeField(auto_now=True)

    objects = ChatManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['participant1', 'participant2'], name='symmetric chat')
        ]


class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_messages')
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    chatbox = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')