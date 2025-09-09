import React, { useState } from 'react';
import { Input, Button } from 'antd';
import UploadFile from '@/components/upload';
import styles from './index.module.less';
const Chatbox = () => {
  const [inputValue, setInputValue] = useState('');
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };
  const handleSubmit = () => {
    console.log(inputValue);
  };

  return (
    <>
      <Input
        defaultValue={inputValue}
        className={styles.input}
        onChange={handleInputChange}
      />
      <UploadFile />
      <Button
        type='primary'
        className={styles.submitButton}
        onClick={handleSubmit}
      >
        Submit
      </Button>
    </>
  );
};
export default Chatbox;
