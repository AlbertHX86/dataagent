import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Card,
  Input,
  Button,
  message,
  Space,
  Typography,
  Spin,
  Row,
  Col,
  Descriptions,
  Tag,
  Alert,
} from 'antd';
import {
  ThunderboltOutlined,
  FileTextOutlined,
  BarChartOutlined,
} from '@ant-design/icons';
import DataUploader from '../components/DataUploader';
import ChartRenderer from '../components/ChartRenderer';
import {
  analyzeData,
  getDatasetInfo,
  DatasetInfo,
  AnalysisResult,
} from '../services/api';
import './AnalysisPage.css';

const { Title, Paragraph, Text } = Typography;
const { TextArea } = Input;

const AnalysisPage: React.FC = () => {
  const { datasetId } = useParams<{ datasetId: string }>();
  const [dataset, setDataset] = useState<DatasetInfo | null>(null);
  const [userQuery, setUserQuery] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  useEffect(() => {
    if (datasetId) {
      loadDataset(datasetId);
    }
  }, [datasetId]);

  const loadDataset = async (id: string) => {
    try {
      const data = await getDatasetInfo(id);
      setDataset(data);
    } catch (error: any) {
      message.error('加载数据集失败');
    }
  };

  const handleAnalyze = async () => {
    if (!dataset) {
      message.error('请先上传数据集');
      return;
    }

    if (!userQuery.trim()) {
      message.error('请输入分析需求');
      return;
    }

    setAnalyzing(true);
    try {
      const analysisResult = await analyzeData(
        dataset.id,
        userQuery,
        dataset.description
      );
      setResult(analysisResult);
      message.success('分析完成！');
    } catch (error: any) {
      message.error(error.response?.data?.detail || '分析失败');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="analysis-page">
      <Title level={2}>
        <BarChartOutlined /> 数据分析
      </Title>
      <Paragraph>
        上传您的数据，描述分析需求，AI将自动为您生成全面的数据分析报告和可视化图表。
      </Paragraph>

      {!dataset ? (
        <DataUploader onUploadSuccess={setDataset} />
      ) : (
        <>
          {/* 数据集信息 */}
          <Card title="数据集信息" style={{ marginBottom: 24 }}>
            <Descriptions column={{ xs: 1, sm: 2, md: 3 }}>
              <Descriptions.Item label="文件名">
                {dataset.filename}
              </Descriptions.Item>
              <Descriptions.Item label="格式">
                <Tag color="blue">{dataset.format.toUpperCase()}</Tag>
              </Descriptions.Item>
              <Descriptions.Item label="行数">
                {dataset.rows.toLocaleString()}
              </Descriptions.Item>
              <Descriptions.Item label="列数">
                {dataset.columns}
              </Descriptions.Item>
              <Descriptions.Item label="上传时间">
                {new Date(dataset.upload_time).toLocaleString()}
              </Descriptions.Item>
            </Descriptions>

            {dataset.description && (
              <div style={{ marginTop: 16 }}>
                <Text strong>数据描述：</Text>
                <Paragraph>{dataset.description}</Paragraph>
              </div>
            )}

            <div style={{ marginTop: 16 }}>
              <Text strong>列名：</Text>
              <div style={{ marginTop: 8 }}>
                {dataset.column_names.map((col) => (
                  <Tag key={col} color="default" style={{ marginBottom: 8 }}>
                    {col} ({dataset.data_types[col]})
                  </Tag>
                ))}
              </div>
            </div>
          </Card>

          {/* 分析需求输入 */}
          {!result && (
            <Card title="描述您的分析需求" style={{ marginBottom: 24 }}>
              <Space direction="vertical" style={{ width: '100%' }} size="large">
                <Alert
                  message="提示"
                  description="用自然语言描述您想要的分析。例如：'分析销售数据的趋势和分布'、'找出影响价格的主要因素'、'对比各个类别的统计数据'等。"
                  type="info"
                  showIcon
                  icon={<FileTextOutlined />}
                />

                <TextArea
                  placeholder="请输入您的分析需求...&#10;例如：我想分析这些数据的整体分布情况，找出变量之间的相关性，并查看是否有明显的趋势。"
                  rows={6}
                  value={userQuery}
                  onChange={(e) => setUserQuery(e.target.value)}
                  maxLength={500}
                  showCount
                />

                <Button
                  type="primary"
                  size="large"
                  icon={<ThunderboltOutlined />}
                  onClick={handleAnalyze}
                  loading={analyzing}
                  block
                >
                  {analyzing ? '分析中...' : '开始分析'}
                </Button>
              </Space>
            </Card>
          )}

          {/* 分析结果 */}
          {analyzing && (
            <Card>
              <div style={{ textAlign: 'center', padding: '60px 0' }}>
                <Spin size="large" />
                <Paragraph style={{ marginTop: 24, fontSize: 16 }}>
                  正在分析数据，请稍候...
                </Paragraph>
              </div>
            </Card>
          )}

          {result && (
            <div className="analysis-results">
              {/* 分析摘要 */}
              <Card
                title="分析摘要"
                style={{ marginBottom: 24 }}
                extra={
                  <Button onClick={() => setResult(null)}>重新分析</Button>
                }
              >
                <Paragraph style={{ fontSize: 16, lineHeight: 1.8 }}>
                  {result.summary}
                </Paragraph>

                <div style={{ marginTop: 24 }}>
                  <Title level={5}>关键洞察</Title>
                  <ul style={{ lineHeight: 2 }}>
                    {result.insights.map((insight, index) => (
                      <li key={index}>
                        <Text>{insight}</Text>
                      </li>
                    ))}
                  </ul>
                </div>
              </Card>

              {/* 可视化图表 */}
              <Title level={3} style={{ marginBottom: 24 }}>
                数据可视化
              </Title>
              <Row gutter={[16, 16]}>
                {result.charts.map((chart, index) => (
                  <Col xs={24} lg={12} key={index}>
                    <ChartRenderer chart={chart} />
                  </Col>
                ))}
              </Row>

              {/* 统计数据 */}
              <Card title="统计数据" style={{ marginTop: 24 }}>
                <pre style={{ maxHeight: 400, overflow: 'auto' }}>
                  {JSON.stringify(result.statistics, null, 2)}
                </pre>
              </Card>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default AnalysisPage;

