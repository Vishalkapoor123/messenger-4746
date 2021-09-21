import React from "react";
import { Box } from "@material-ui/core";
import { BadgeAvatar, ChatContent } from "../Sidebar";
import { makeStyles } from "@material-ui/core/styles";
import { setActiveChat } from "../../store/activeConversation";
import { connect } from "react-redux";
import Badge from "@material-ui/core/Badge";
import { setMessageToRead } from "../../store/utils/thunkCreators";

const useStyles = makeStyles((theme) => ({
  root: {
    borderRadius: 8,
    height: 80,
    boxShadow: "0 2px 10px 0 rgba(88,133,196,0.05)",
    marginBottom: 10,
    display: "flex",
    alignItems: "center",
    "&:hover": {
      cursor: "grab",
    },
  },
  badge: {
    marginRight: 20,
  },
}));

const Chat = (props) => {
  const classes = useStyles();
  const { conversation, setMessageToRead } = props;
  const { otherUser } = conversation;

  const handleClick = async (conversation) => {
    await props.setActiveChat(conversation.otherUser.username);
    //mark messages to read when set to active chat
    if (conversation.id) {
      setMessageToRead(conversation.id);
    }
  };

  return (
    <Box onClick={() => handleClick(conversation)} className={classes.root}>
      <BadgeAvatar
        photoUrl={otherUser.photoUrl}
        username={otherUser.username}
        online={otherUser.online}
        sidebar={true}
      />
      <ChatContent conversation={conversation} />
      {conversation.unread_count > 0 && (
        <Badge
          className={classes.badge}
          badgeContent={conversation.unread_count}
          color="primary"
        />
      )}
    </Box>
  );
};

const mapDispatchToProps = (dispatch) => {
  return {
    setActiveChat: (id) => {
      dispatch(setActiveChat(id));
    },
    setMessageToRead: (conversationId) => {
      dispatch(setMessageToRead(conversationId));
    },
  };
};

export default connect(null, mapDispatchToProps)(Chat);
