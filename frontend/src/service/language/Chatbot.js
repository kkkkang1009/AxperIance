import Tab from '@mui/material/Tab';

function Chatbot(props) {
    return (
        <div>
            <p>Chatbot</p>
            <Tab
                component="a"
                onClick={(event) => {
                event.preventDefault();
                }}
                {...props}
            />
        </div>
      
    );
  }

  export default Chatbot;