const SET_READ_STATUS = "SET_READ_STATUS";

export const setReadStatus = (status) => {
  return {
    type: SET_READ_STATUS,
    status
  };
};

const reducer = (state = {unread_count:0}, action) => {
  switch (action.type) {
    case SET_READ_STATUS: {
      return action.status;
    }
    default:
      return state;
  }
};

export default reducer;
