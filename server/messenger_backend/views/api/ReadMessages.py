from django.contrib.auth.middleware import get_user
from django.http import HttpResponse
from messenger_backend.models import Conversation, Message
from rest_framework.views import APIView


class ReadMessages(APIView):
    """expects { conversationId } in body"""

    def post(self, request):
        try:
            user = get_user(request)

            if user.is_anonymous:
                return HttpResponse(status=401)

            body = request.data
            conversation_id = body.get("conversationId")

            conversation = Conversation.objects.filter(id=conversation_id).first()
            messages = Message.objects.filter(conversation = conversation)
            messages.update(read = True)
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=500)
