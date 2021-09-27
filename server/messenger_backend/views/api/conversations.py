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
                latestMessageRead = ""
                #set unread messages count
                for message in convo.messages.all():
                    if(message.read == False and message.senderId != user_id ):
                        unread_count+=1
                    if(message.read == True and message.senderId==user_id):
                        latestMessageRead = message.id

                #unread messages count and latest message for respective chats
                convo_dict["unreadCount"] = unread_count
                convo_dict["latestMessageRead"] = [latestMessageRead]
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
            #Protecting route if user is not anonynous and not belong to that particular conversation
            if(sender not in [conversation.user1.id, conversation.user2.id]):
                return HttpResponse(status=401)
            #Get recipient
            if(conversation.user1.id == sender):
                recipient = conversation.user2.id
            else:
                recipient = conversation.user1.id

            messages = Message.objects.filter(conversation = conversation)
            #update read status for messages from the other user, thats why sender is excluded
            messages.exclude(senderId = sender).update(read = True)
            #Get latest read message by user one and user two, if present return theeir IDs
            lastMessageReadUserOne = messages.filter(senderId = sender, read = True).last()
            lastMessageReadUserTwo = messages.filter(senderId =recipient, read= True).last()
            if(lastMessageReadUserOne is not None):
                lastMessageReadIdOne = lastMessageReadUserOne.id
            else:
                lastMessageReadIdOne = None
            if(lastMessageReadUserTwo is not None):
                lastMessageReadIdTwo = lastMessageReadUserTwo.id
            else:
                lastMessageReadIdTwo = None
            return JsonResponse({"conversationId":conversation_id, "latestMessageRead":[lastMessageReadIdOne,lastMessageReadIdTwo], "recipientId":recipient})
        except Exception as e:
            return HttpResponse(status=500)
