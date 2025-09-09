import { useState } from 'react';
import RouterRoot from './routes';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <RouterRoot />
    </>
  );
}

export default App;
