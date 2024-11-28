import React from 'react';
import Video from '../src/components/Video.js'
import Header from '../src/components/Header.js';
import ShowLetter from './components/ShowLetter.js';

function App () {
  return (
    <>
      <Header />
      <div className='flex justify-center gap-5 mx-3'>
        <Video/>
        <ShowLetter/>
      </div>

    </>
  );
};

export default App;
