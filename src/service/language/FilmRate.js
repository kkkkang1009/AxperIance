import Tab from '@mui/material/Tab';

function FilmRate(props) {
    return (
        <div>
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

  export default FilmRate;