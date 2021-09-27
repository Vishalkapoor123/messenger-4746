from django.db import models
from django.db.models import Q

from . import utils
from .user import User


class Conversation(utils.CustomModel):

    title = models.CharField(null=True, max_length=255)
    members = models.ManyToManyField(User, db_column="members")
    createdAt = models.DateTimeField(auto_now_add=True, db_index=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # find conversation given id
    def find_conversation(id):
        # return conversation or None if it doesn't exist
        try:
            return Conversation.objects.get(Q(id=id))
        except Conversation.DoesNotExist:
            return None
