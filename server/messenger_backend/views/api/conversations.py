from django.contrib.auth.middleware import get_user
from django.db.models import Max, Q
from django.db.models.query import Prefetch
from django.http import HttpResponse, JsonResponse
from messenger_backend.models import Conversation, Message
from online_users import online_users
from rest_framework.views import APIView
from rest_framework.request import Request


class Conversations(APIView):
    """get all conversations for a user, include latest message text for preview, and all messages
    include other user model so we have info on username/profile pic (don't include current user info)
    TODO: for scalability, implement lazy loading"""

    def get(self, request: Request):
        try:
            user = get_user(request)

            if user.is_anonymous:
                return HttpResponse(status=401)
            user_id = user.id

            conversations = (
                Conversation.objects.filter(Q(user1=user_id) | Q(user2=user_id))
                .prefetch_related(
                    Prefetch(
                        "messages", queryset=Message.objects.order_by("createdAt")
                    )
                )
                .all()
            )

            conversations_response = []

            for convo in conversations:
                convo_dict = {
                    "id": convo.id,
                    "messages": [
                        message.to_dict(["id", "text", "senderId", "createdAt", "read"])
                        for message in convo.messages.all()
                    ],
                }

                unread_count = 0
                #set unread messages count
                for message in convo.messages.all():
                    if(message.read == False and message.senderId != user_id ):
                        unread_count+=1

                convo_dict["unread_count"] = unread_count
                # set properties for notification count and last message preview which will the lastest one
                convo_dict["latestMessageText"] = convo_dict["messages"][-1]["text"]

                # set a property "otherUser" so that frontend will have easier access
                user_fields = ["id", "username", "photoUrl"]
                if convo.user1 and convo.user1.id != user_id:
                    convo_dict["otherUser"] = convo.user1.to_dict(user_fields)
                elif convo.user2 and convo.user2.id != user_id:
                    convo_dict["otherUser"] = convo.user2.to_dict(user_fields)

                # set property for online status of the other user
                if convo_dict["otherUser"]["id"] in online_users:
                    convo_dict["otherUser"]["online"] = True
                else:
                    convo_dict["otherUser"]["online"] = False

                conversations_response.append(convo_dict)
            #sort messages from latest to oldest
            conversations_response.sort(
                key=lambda convo: convo["messages"][-1]["createdAt"],
                reverse=True,
            )
            return JsonResponse(
                conversations_response,
                safe=False,
            )
        except Exception as e:
            return HttpResponse(status=500)

class ReadMessages(APIView):
    """expects {conversationId } in body"""

    def put(self, request):
        try:
            user = get_user(request)

            if user.is_anonymous:
                return HttpResponse(status=401)
            sender = user.id
            body = request.data
            conversation_id = body.get("conversationId")

            conversation = Conversation.objects.filter(id=conversation_id).first()
            messages = Message.objects.filter(conversation = conversation).exclude(senderId = sender)
            #update read status for messages from the other user, thats why sender is excluded
            messages.update(read = True)
            unread_count = 0
            #set unread messages count
            for message in messages:
              if(message.read == False and message.senderId != sender ):
                unread_count+=1
            conversationId = list(messages.values("conversation_id"))[0]["conversation_id"]
            return JsonResponse({"conversation_id":conversationId, "unread_count":unread_count})
        except Exception as e:
            return HttpResponse(status=500)
