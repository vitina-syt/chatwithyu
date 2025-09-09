import React from 'react';
// import { UploadOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import { Button, message, Upload } from 'antd';
import styles from './index.module.less';

const UploadFile = () => {
  const props: UploadProps = {
    name: 'file',
    action: 'http://localhost:8000/api/upload', // 修改为本地后端地址
    // headers: {
    //   'Content-Type': 'multipart/form-data',
    // },
    beforeUpload: (file) => {
      // 文件类型检查
      const isPDF = file.type === 'application/pdf';
      if (!isPDF) {
        message.error('只能上传 PDF 文件!');
        return false;
      }
      
      // 文件大小检查 (10MB)
      const isLt10M = file.size / 1024 / 1024 < 10;
      if (!isLt10M) {
        message.error('文件大小不能超过 10MB!');
        return false;
      }
      
      return true;
    },
  };
  const handleChange = (info: any) => {
    console.log('文件info', info);
    if (info.file.status !== 'uploading') {
      console.log(info.file, info.fileList);
    }
    if (info.file.status === 'done') {
      message.success(`${info.file.name} file uploaded successfully`);
    } else if (info.file.status === 'error') {
      message.error(`${info.file.name} file upload failed.`);
    }
  };
  return (
    <>
      <Upload onChange={info => handleChange(info)} {...props}>
        <Button className={styles.uploadButton}>文件上传</Button>
      </Upload>
    </>
  );
};

export default UploadFile;
