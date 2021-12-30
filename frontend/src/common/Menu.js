import * as React from 'react';
import { render } from 'react-dom';
//import { Router, Route, IndexRoute, Link } from 'react-router';
//import { withRouter } from 'react-router-dom';
import { Link } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
// import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import TranslateIcon from '@mui/icons-material/Translate';
import MenuIcon from '@mui/icons-material/Menu';

import SwipeableDrawer from '@mui/material/SwipeableDrawer';
import Button from '@mui/material/Button';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';

//import Router from "next/router";

function Menu() {

  const [state, setState] = React.useState({
    top: false,
    left: false,
    bottom: false,
    right: false,
    title: "",
  });

  const resetTitleName = (titleValue) => {
    console.log(titleValue);
    //titleName = title;
    /*setState({
      top: false,
      left: false,
      bottom: false,
      right: false,
      title: titleValue,
    })*/
    setState({ ...state, ["title"]: titleValue });
    console.log(state);
  };

  const toggleDrawer = (anchor, open) => (event) => {
    if (
      event &&
      event.type === 'keydown' &&
      (event.key === 'Tab' || event.key === 'Shift')
    ) {
      return;
    }

    setState({ ...state, [anchor]: open });
  };

  const list = (anchor) => (
    <Box
      sx={{ width: anchor === 'top' || anchor === 'bottom' ? 'auto' : 250 }}
      role="presentation"
      onClick={toggleDrawer(anchor, false)}
      onKeyDown={toggleDrawer(anchor, false)}
    >
      <List>
        {/* {['Film Rate', 'Chatbot', 'MRC'].map((text, index) => (
          <ListItem button key={text}>
            <ListItemIcon>
              {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
            </ListItemIcon>
            <ListItemText primary={text} />
          </ListItem>
        ))} */}
        <ListItem button key={"Film Rate"}>
          <ListItemIcon>
            <InboxIcon />
          </ListItemIcon>
          <Link to="/filmrate" onClick={resetTitleName.bind(null, "Film Rate")} style={{ textDecoration: 'none' }}>
            <ListItemText primary={"Film Rate"} />
          </Link>
        </ListItem>
        <ListItem button key={"Chatbot"}>
          <ListItemIcon>
            <MailIcon />
          </ListItemIcon>
          <Link to="/chatbot" onClick={resetTitleName.bind(null, "Chatbot")} style={{ textDecoration: 'none' }}>
            <ListItemText primary={"Chatbot"} />
          </Link>
        </ListItem>
      </List>
      <Divider />
      {/* <List>
        {['Settings'].map((text, index) => (
          <ListItem button key={text}>
            <ListItemIcon>
              {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
            </ListItemIcon>
            <ListItemText primary={text} />
          </ListItem>
        ))}
      </List> */}
    </Box>
  );

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
          >
            <div>
              <MenuIcon onClick={toggleDrawer('left', true)}>{'left'}</MenuIcon>
              <SwipeableDrawer
                anchor={'left'}
                open={state['left']}
                onClose={toggleDrawer('left', false)}
                onOpen={toggleDrawer('left', true)}
              >
                {list('left')}
              </SwipeableDrawer>
            </div>

          </IconButton>
          {/* <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Language
          </Typography>
          <Button color="inherit">Login</Button> */}
          <div>{state.title}</div>
          {/* <div>{state['title']}</div> */}
        </Toolbar>
      </AppBar>
    </Box>
  );
}

export default Menu;
