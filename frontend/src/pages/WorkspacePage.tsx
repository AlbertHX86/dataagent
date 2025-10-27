import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  Row,
  Col,
  Typography,
  Button,
  Empty,
  Tag,
  Space,
  Modal,
  Tooltip,
} from 'antd';
import {
  FolderOutlined,
  BarChartOutlined,
  LineChartOutlined,
  DeleteOutlined,
  EyeOutlined,
  ClockCircleOutlined,
} from '@ant-design/icons';
import { getWorkRecords, deleteWorkRecord, WorkRecord } from '../services/api';
import './WorkspacePage.css';

const { Title, Paragraph, Text } = Typography;

const WorkspacePage: React.FC = () => {
  const navigate = useNavigate();
  const [records, setRecords] = useState<WorkRecord[]>([]);
  const [loading, setLoading] = useState(true);

  // 模拟用户ID（实际应从认证系统获取）
  const userId = 'demo-user';

  useEffect(() => {
    loadRecords();
  }, []);

  const loadRecords = async () => {
    setLoading(true);
    try {
      const data = await getWorkRecords(userId);
      setRecords(data);
    } catch (error) {
      // 如果用户不存在，显示空状态
      setRecords([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (recordId: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这条工作记录吗？',
      okText: '确定',
      cancelText: '取消',
      onOk: async () => {
        try {
          await deleteWorkRecord(userId, recordId);
          setRecords(records.filter((r) => r.record_id !== recordId));
        } catch (error) {
          console.error('删除失败', error);
        }
      },
    });
  };

  const handleView = (record: WorkRecord) => {
    if (record.type === 'analysis') {
      navigate(`/analysis/${record.result_id}`);
    } else if (record.type === 'prediction') {
      navigate(`/prediction/${record.result_id}`);
    }
  };

  const getTypeIcon = (type: string) => {
    return type === 'analysis' ? (
      <BarChartOutlined style={{ fontSize: 32, color: '#1890ff' }} />
    ) : (
      <LineChartOutlined style={{ fontSize: 32, color: '#52c41a' }} />
    );
  };

  const getTypeTag = (type: string) => {
    return type === 'analysis' ? (
      <Tag color="blue">数据分析</Tag>
    ) : (
      <Tag color="green">预测分析</Tag>
    );
  };

  if (loading) {
    return (
      <div className="workspace-page">
        <Title level={2}>
          <FolderOutlined /> 我的工作
        </Title>
        <Card loading={true} />
      </div>
    );
  }

  return (
    <div className="workspace-page">
      <div className="workspace-header">
        <div>
          <Title level={2}>
            <FolderOutlined /> 我的工作
          </Title>
          <Paragraph>
            这里保存了您的所有数据分析和预测工作记录
          </Paragraph>
        </div>
        <Space>
          <Button
            type="primary"
            icon={<BarChartOutlined />}
            onClick={() => navigate('/analysis')}
          >
            新建分析
          </Button>
          <Button
            icon={<LineChartOutlined />}
            onClick={() => navigate('/prediction')}
          >
            新建预测
          </Button>
        </Space>
      </div>

      {records.length === 0 ? (
        <Card>
          <Empty
            description="暂无工作记录"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          >
            <Space>
              <Button
                type="primary"
                icon={<BarChartOutlined />}
                onClick={() => navigate('/analysis')}
              >
                开始分析
              </Button>
              <Button
                icon={<LineChartOutlined />}
                onClick={() => navigate('/prediction')}
              >
                开始预测
              </Button>
            </Space>
          </Empty>
        </Card>
      ) : (
        <Row gutter={[16, 16]}>
          {records.map((record) => (
            <Col xs={24} sm={12} lg={8} xl={6} key={record.record_id}>
              <Card
                hoverable
                className="work-record-card"
                cover={
                  <div className="record-cover">
                    {getTypeIcon(record.type)}
                  </div>
                }
                actions={[
                  <Tooltip title="查看">
                    <EyeOutlined
                      key="view"
                      onClick={() => handleView(record)}
                    />
                  </Tooltip>,
                  <Tooltip title="删除">
                    <DeleteOutlined
                      key="delete"
                      onClick={() => handleDelete(record.record_id)}
                    />
                  </Tooltip>,
                ]}
              >
                <Card.Meta
                  title={
                    <div>
                      {getTypeTag(record.type)}
                      <Title level={5} style={{ marginTop: 8 }}>
                        {record.title}
                      </Title>
                    </div>
                  }
                  description={
                    <Space direction="vertical" style={{ width: '100%' }}>
                      <Text ellipsis={{ tooltip: record.description }}>
                        {record.description}
                      </Text>
                      <Text type="secondary" style={{ fontSize: 12 }}>
                        <ClockCircleOutlined />{' '}
                        {new Date(record.created_at).toLocaleDateString()}
                      </Text>
                      <Text type="secondary" style={{ fontSize: 12 }}>
                        数据集: {record.dataset_name}
                      </Text>
                    </Space>
                  }
                />
              </Card>
            </Col>
          ))}
        </Row>
      )}
    </div>
  );
};

export default WorkspacePage;

