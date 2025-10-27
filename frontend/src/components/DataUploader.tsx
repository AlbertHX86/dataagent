import React, { useState } from 'react';
import { Upload, Button, message, Input, Card, Space } from 'antd';
import { InboxOutlined, UploadOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import { uploadDataset, DatasetInfo } from '../services/api';

const { Dragger } = Upload;
const { TextArea } = Input;

interface DataUploaderProps {
  onUploadSuccess?: (dataset: DatasetInfo) => void;
}

const DataUploader: React.FC<DataUploaderProps> = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [description, setDescription] = useState('');
  const [fileList, setFileList] = useState<any[]>([]);

  const handleUpload = async () => {
    if (fileList.length === 0) {
      message.error('请选择文件');
      return;
    }

    const file = fileList[0];
    setUploading(true);

    try {
      const dataset = await uploadDataset(file, description);
      message.success('文件上传成功！');
      setFileList([]);
      setDescription('');
      onUploadSuccess?.(dataset);
    } catch (error: any) {
      message.error(error.response?.data?.detail || '文件上传失败');
    } finally {
      setUploading(false);
    }
  };

  const uploadProps: UploadProps = {
    name: 'file',
    multiple: false,
    fileList,
    beforeUpload: (file) => {
      const isValidFormat =
        file.name.endsWith('.csv') ||
        file.name.endsWith('.json') ||
        file.name.endsWith('.txt');

      if (!isValidFormat) {
        message.error('只支持CSV、JSON和TXT格式的文件！');
        return false;
      }

      const isLt100M = file.size / 1024 / 1024 < 100;
      if (!isLt100M) {
        message.error('文件大小不能超过100MB！');
        return false;
      }

      setFileList([file]);
      return false;
    },
    onRemove: () => {
      setFileList([]);
    },
  };

  return (
    <Card title="上传数据" style={{ marginBottom: 24 }}>
      <Space direction="vertical" style={{ width: '100%' }} size="large">
        <Dragger {...uploadProps}>
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">点击或拖拽文件到此区域上传</p>
          <p className="ant-upload-hint">
            支持CSV、JSON、TXT格式，文件大小不超过100MB
          </p>
        </Dragger>

        <TextArea
          placeholder="请描述您的数据（可选）&#10;例如：这是一个销售数据集，包含过去一年的销售记录..."
          rows={4}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <Button
          type="primary"
          onClick={handleUpload}
          loading={uploading}
          disabled={fileList.length === 0}
          icon={<UploadOutlined />}
          block
          size="large"
        >
          {uploading ? '上传中...' : '开始上传'}
        </Button>
      </Space>
    </Card>
  );
};

export default DataUploader;

