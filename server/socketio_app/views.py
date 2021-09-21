async_mode = None

import os

import socketio
from online_users import online_users

basedir = os.path.dirname(os.path.realpath(__file__))
#Allowing all hosts to connect, change it as per the host on the client side
sio = socketio.Server(async_mode=async_mode, logger=False,cors_allowed_origins="*")
thread = None


@sio.event
def connect(sid, environ):
    sio.emit("my_response", {"data": "Connected", "count": 0}, room=sid)

#add and store users with sid in a dictionary
@sio.on("go-online")
def go_online(sid, user_id):
    online_users[user_id] = sid
    sio.emit("add-online-user", user_id)

#emit new message for online user else emit nothing
@sio.on("new-message")
def new_message(sid, message):
    for user in online_users.keys():
        if(user == message["recipientId"]):
            recipient_sid = online_users[user]
            sio.emit("new-message",
            {"message": message["message"], "sender": message["sender"]},
            skip_sid = sid,
            to = recipient_sid
            )

#remove user from dictionary
@sio.on("logout")
def logout(sid, user_id):
    if user_id in online_users:
        del online_users[user_id]
    sio.emit("remove-offline-user", user_id)
