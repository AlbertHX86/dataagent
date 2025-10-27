import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Row, Col, Card, Button, Typography, Space, Statistic } from 'antd';
import {
  BarChartOutlined,
  LineChartOutlined,
  RocketOutlined,
  SafetyOutlined,
  ThunderboltOutlined,
  SmileOutlined,
} from '@ant-design/icons';
import DataUploader from '../components/DataUploader';
import { DatasetInfo } from '../services/api';
import './HomePage.css';

const { Title, Paragraph } = Typography;

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const handleUploadSuccess = (dataset: DatasetInfo) => {
    // 上传成功后跳转到分析页面
    navigate(`/analysis/${dataset.id}`);
  };

  const features = [
    {
      icon: <ThunderboltOutlined style={{ fontSize: 48, color: '#1890ff' }} />,
      title: 'AI驱动分析',
      description: '使用自然语言描述需求，AI自动完成复杂数据分析',
    },
    {
      icon: <BarChartOutlined style={{ fontSize: 48, color: '#52c41a' }} />,
      title: '自动可视化',
      description: '智能生成多种统计图表，直观展示数据洞察',
    },
    {
      icon: <LineChartOutlined style={{ fontSize: 48, color: '#fa8c16' }} />,
      title: '智能预测',
      description: '自动验证数据假设，选择最佳预测模型',
    },
    {
      icon: <SafetyOutlined style={{ fontSize: 48, color: '#eb2f96' }} />,
      title: '数据安全',
      description: '本地处理，保护您的数据隐私和安全',
    },
  ];

  return (
    <div className="home-page">
      {/* Hero Section */}
      <div className="hero-section">
        <Space direction="vertical" size="large" align="center">
          <RocketOutlined style={{ fontSize: 80, color: '#1890ff' }} />
          <Title level={1} style={{ marginBottom: 0 }}>
            欢迎使用数据分析Agent
          </Title>
          <Paragraph style={{ fontSize: 18, color: '#666', maxWidth: 600, textAlign: 'center' }}>
            一个智能化的数据分析平台，帮助您轻松完成数据上传、分析、可视化和预测任务。
            无需编程，通过自然语言即可获得专业级的分析结果。
          </Paragraph>
        </Space>
      </div>

      {/* Upload Section */}
      <Row gutter={[24, 24]} style={{ marginTop: 48 }}>
        <Col xs={24} lg={16}>
          <DataUploader onUploadSuccess={handleUploadSuccess} />
        </Col>
        <Col xs={24} lg={8}>
          <Card title="快速开始" className="quick-start-card">
            <Space direction="vertical" style={{ width: '100%' }} size="middle">
              <Button
                type="primary"
                size="large"
                block
                icon={<BarChartOutlined />}
                onClick={() => navigate('/analysis')}
              >
                数据分析
              </Button>
              <Button
                size="large"
                block
                icon={<LineChartOutlined />}
                onClick={() => navigate('/prediction')}
              >
                预测分析
              </Button>
              <Button
                size="large"
                block
                icon={<SmileOutlined />}
                onClick={() => navigate('/workspace')}
              >
                我的工作
              </Button>
            </Space>

            <div style={{ marginTop: 24 }}>
              <Statistic
                title="支持的数据格式"
                value="CSV, JSON, TXT"
                valueStyle={{ fontSize: 16 }}
              />
            </div>
          </Card>
        </Col>
      </Row>

      {/* Features Section */}
      <div style={{ marginTop: 64 }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 48 }}>
          核心功能
        </Title>
        <Row gutter={[24, 24]}>
          {features.map((feature, index) => (
            <Col xs={24} sm={12} lg={6} key={index}>
              <Card className="feature-card" hoverable>
                <Space direction="vertical" align="center" style={{ width: '100%' }}>
                  {feature.icon}
                  <Title level={4}>{feature.title}</Title>
                  <Paragraph style={{ textAlign: 'center', color: '#666' }}>
                    {feature.description}
                  </Paragraph>
                </Space>
              </Card>
            </Col>
          ))}
        </Row>
      </div>

      {/* Steps Section */}
      <div style={{ marginTop: 64 }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: 48 }}>
          使用步骤
        </Title>
        <Row gutter={[24, 24]}>
          <Col xs={24} md={6}>
            <Card className="step-card">
              <div className="step-number">1</div>
              <Title level={4}>上传数据</Title>
              <Paragraph>支持CSV、JSON、TXT等格式</Paragraph>
            </Card>
          </Col>
          <Col xs={24} md={6}>
            <Card className="step-card">
              <div className="step-number">2</div>
              <Title level={4}>描述需求</Title>
              <Paragraph>用自然语言描述分析目标</Paragraph>
            </Card>
          </Col>
          <Col xs={24} md={6}>
            <Card className="step-card">
              <div className="step-number">3</div>
              <Title level={4}>查看结果</Title>
              <Paragraph>获得可视化图表和洞察</Paragraph>
            </Card>
          </Col>
          <Col xs={24} md={6}>
            <Card className="step-card">
              <div className="step-number">4</div>
              <Title level={4}>高级分析</Title>
              <Paragraph>使用预测功能进行深入分析</Paragraph>
            </Card>
          </Col>
        </Row>
      </div>
    </div>
  );
};

export default HomePage;

