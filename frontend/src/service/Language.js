import * as React from 'react';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import FilmRate from './language/FilmRate';



function Language() {
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Tabs value={value} onChange={handleChange} aria-label="nav tabs example">
        <FilmRate label="Film Rate" href="/drafts" />
        <FilmRate label="Chatbot" href="/trash" />
        <FilmRate label="MRC" href="/spam" />
      </Tabs>
    </Box>
  );
}

export default Language;