import { setMessageToRead } from "./thunkCreators";
import store from "..";

export const addMessageToStore = (state, payload) => {
  const { message, sender, activeConversation } = payload;
  // if sender isn't null, that means the message needs to be put in a brand new convo
  if (sender !== null) {
    const newConvo = {
      id: message.conversationId,
      otherUser: sender,
      messages: [message],
    };
    newConvo.latestMessageText = message.text;
    //for new convo unreadCount have to be initiated to one and latest read messages will be none
    newConvo.unreadCount = 1;
    newConvo.latestMessageRead = [];
    return [newConvo, ...state];
  }
  //Return updated conversation, so as to get real-time updates
  return state.map((convo) => {
    if (convo.id === message.conversationId) {
      const convoCopy = { ...convo };
      convoCopy.messages.push(message);
      convoCopy.latestMessageText = message.text;
      //if users active conversation is the one opened, then emit an event fromt the recipient side to mark read on the sender side
      //and dont increase unread count on the recipient side
      if (
        activeConversation === convoCopy.otherUser.username &&
        convoCopy.otherUser.id === message.senderId
      ) {
        store.dispatch(setMessageToRead(convoCopy.id));
      } else {
        convoCopy.unreadCount +=
          convoCopy.otherUser.id === message.senderId ? 1 : 0;
      }
      return convoCopy;
    } else {
      return convo;
    }
  });
};

export const addOnlineUserToStore = (state, id) => {
  return state.map((convo) => {
    if (convo.otherUser.id === id) {
      const convoCopy = { ...convo };
      convoCopy.otherUser.online = true;
      return convoCopy;
    } else {
      return convo;
    }
  });
};

export const removeOfflineUserFromStore = (state, id) => {
  return state.map((convo) => {
    if (convo.otherUser.id === id) {
      const convoCopy = { ...convo };
      convoCopy.otherUser.online = false;
      return convoCopy;
    } else {
      return convo;
    }
  });
};

export const addSearchedUsersToStore = (state, users) => {
  const currentUsers = {};

  // make table of current users so we can lookup faster
  state.forEach((convo) => {
    currentUsers[convo.otherUser.id] = true;
  });

  const newState = [...state];
  users.forEach((user) => {
    // only create a fake convo if we don't already have a convo with this user
    if (!currentUsers[user.id]) {
      let fakeConvo = { otherUser: user, messages: [] };
      newState.push(fakeConvo);
    }
  });

  return newState;
};

export const addNewConvoToStore = (state, recipientId, message) => {
  return state.map((convo) => {
    if (convo.otherUser.id === recipientId) {
      const convoCopy = { ...convo };
      convoCopy.id = message.conversationId;
      convoCopy.messages.push(message);
      convoCopy.latestMessageText = message.text;
      convoCopy.unreadCount = 0;
      convoCopy.latestMessageRead = [];
      return convoCopy;
    } else {
      return convo;
    }
  });
};

export const markReadInStore = (state, payload) => {
  return state.map((convo) => {
    if (convo.id === payload.conversationId) {
      const newConvo = { ...convo };
      if (payload.recipientId) {
        newConvo.unreadCount = 0;
      }
      //Keeping backend in sync with the status
      newConvo.messages.forEach((message) => {
        message.read = true;
      });
      newConvo.latestMessageRead = payload.latestMessageRead;
      return newConvo;
    } else {
      return convo;
    }
  });
};
