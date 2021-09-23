import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Box, Typography } from "@material-ui/core";
import { Avatar } from "@material-ui/core";
const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-end",
  },
  date: {
    fontSize: 11,
    color: "#BECCE2",
    fontWeight: "bold",
    marginBottom: 5,
  },
  text: {
    fontSize: 14,
    color: "#91A3C0",
    letterSpacing: -0.2,
    padding: 8,
    fontWeight: "bold",
  },
  bubble: {
    background: "#F4F6FA",
    borderRadius: "10px 10px 0 10px",
  },
  //adding styles for the avatar to show below read messages
  readAvatar: {
    width: theme.spacing(2.5),
    height: theme.spacing(2.5),
  },
}));

const SenderBubble = (props) => {
  const classes = useStyles();
  const { time, text, otherUser, latestMessageRead } = props;
  return (
    <Box className={classes.root}>
      <Typography className={classes.date}>{time}</Typography>
      <Box className={classes.bubble}>
        <Typography className={classes.text}>{text}</Typography>
      </Box>
      {latestMessageRead && (
        <Avatar
          alt={otherUser.username}
          className={classes.readAvatar}
          src={otherUser.photoUrl}
        ></Avatar>
      )}
    </Box>
  );
};

export default SenderBubble;
