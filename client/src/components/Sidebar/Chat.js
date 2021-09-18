import React,{useState} from "react";
import { Box } from "@material-ui/core";
import { BadgeAvatar, ChatContent } from "../Sidebar";
import { makeStyles } from "@material-ui/core/styles";
import { setActiveChat } from "../../store/activeConversation";
import { connect } from "react-redux";
import Badge from '@material-ui/core/Badge';
import { setMessagesToread } from "../../store/utils/thunkCreators";
import { setReadStatus } from "../../store/readStatus";



const useStyles = makeStyles((theme) => ({
  root: {
    borderRadius: 8,
    height: 80,
    boxShadow: "0 2px 10px 0 rgba(88,133,196,0.05)",
    marginBottom: 10,
    display: "flex",
    alignItems: "center",
    "&:hover": {
      cursor: "grab"
    }
  },
  badge: {
    marginRight: 20
  }
}));


const Chat = (props) => {
  const classes = useStyles();
  const { conversation, unread_count } = props;
  const { otherUser } = conversation;


  const handleClick = async (conversation) => {
    await props.setActiveChat(conversation.otherUser.username);
    props.setReadStatus(conversation.id)
    // console.log(conversation)
    // setUnread(0)
    // axios.post(`/api/conversations/read`, {conversationId:conversation.id}).then(response =>{console.log(response)} )
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
      {unread_count>-15?
      <Badge className={classes.badge} badgeContent={unread_count} color="primary"/>:""}

    </Box>
  );
};

const mapDispatchToProps = (dispatch) => {
  return {
    setActiveChat: (id) => {
      dispatch(setActiveChat(id));
    },
    setReadStatus: (conversationId) => {
      dispatch(setReadStatus(conversationId))
    }
  };
};

export default connect(null, mapDispatchToProps)(Chat);
