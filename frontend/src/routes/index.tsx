import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Chatbox from '../components/chatbox';

const RouterRoot = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Chatbox />} />
      </Routes>
    </BrowserRouter>
  );
};
export default RouterRoot;
