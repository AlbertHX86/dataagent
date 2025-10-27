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
  Select,
  InputNumber,
  Descriptions,
  Tag,
  Alert,
  Row,
  Col,
  Statistic,
} from 'antd';
import {
  LineChartOutlined,
  RocketOutlined,
  CheckCircleOutlined,
  WarningOutlined,
} from '@ant-design/icons';
import DataUploader from '../components/DataUploader';
import ChartRenderer from '../components/ChartRenderer';
import {
  predictData,
  validateTimeSeries,
  getDatasetInfo,
  DatasetInfo,
  PredictionResult,
} from '../services/api';
import './PredictionPage.css';

const { Title, Paragraph, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const PredictionPage: React.FC = () => {
  const { datasetId } = useParams<{ datasetId: string }>();
  const [dataset, setDataset] = useState<DatasetInfo | null>(null);
  const [targetColumn, setTargetColumn] = useState<string>('');
  const [predictionQuery, setPredictionQuery] = useState('');
  const [modelType, setModelType] = useState<string>('');
  const [forecastPeriods, setForecastPeriods] = useState<number>(10);
  const [predicting, setPredicting] = useState(false);
  const [validating, setValidating] = useState(false);
  const [validationResult, setValidationResult] = useState<any>(null);
  const [result, setResult] = useState<PredictionResult | null>(null);

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

  const handleValidate = async () => {
    if (!dataset || !targetColumn) {
      message.error('请先选择目标列');
      return;
    }

    setValidating(true);
    try {
      const validation = await validateTimeSeries(dataset.id, targetColumn);
      setValidationResult(validation);
      
      if (validation.is_valid) {
        message.success('数据验证通过！');
      } else {
        message.warning('数据不完全满足假设，将进行自动转换');
      }
    } catch (error: any) {
      message.error(error.response?.data?.detail || '验证失败');
    } finally {
      setValidating(false);
    }
  };

  const handlePredict = async () => {
    if (!dataset) {
      message.error('请先上传数据集');
      return;
    }

    if (!targetColumn) {
      message.error('请选择目标列');
      return;
    }

    if (!predictionQuery.trim()) {
      message.error('请描述预测需求');
      return;
    }

    setPredicting(true);
    try {
      const predictionResult = await predictData(
        dataset.id,
        targetColumn,
        predictionQuery,
        modelType || undefined,
        forecastPeriods
      );
      setResult(predictionResult);
      message.success('预测完成！');
    } catch (error: any) {
      message.error(error.response?.data?.detail || '预测失败');
    } finally {
      setPredicting(false);
    }
  };

  const numericColumns = dataset?.column_names.filter(
    (col) => dataset.data_types[col] === 'int64' || dataset.data_types[col] === 'float64'
  ) || [];

  return (
    <div className="prediction-page">
      <Title level={2}>
        <LineChartOutlined /> 预测分析
      </Title>
      <Paragraph>
        上传时间序列数据，系统将自动验证数据假设，选择最佳预测模型，并生成未来趋势预测。
      </Paragraph>

      {!dataset ? (
        <DataUploader onUploadSuccess={setDataset} />
      ) : (
        <>
          {/* 数据集信息 */}
          <Card title="数据集信息" style={{ marginBottom: 24 }}>
            <Descriptions column={{ xs: 1, sm: 2 }}>
              <Descriptions.Item label="文件名">
                {dataset.filename}
              </Descriptions.Item>
              <Descriptions.Item label="行数">
                {dataset.rows.toLocaleString()}
              </Descriptions.Item>
            </Descriptions>
          </Card>

          {/* 预测配置 */}
          {!result && (
            <Card title="预测配置" style={{ marginBottom: 24 }}>
              <Space direction="vertical" style={{ width: '100%' }} size="large">
                <div>
                  <Text strong>选择目标列 *</Text>
                  <Select
                    style={{ width: '100%', marginTop: 8 }}
                    placeholder="选择要预测的数值列"
                    value={targetColumn}
                    onChange={setTargetColumn}
                  >
                    {numericColumns.map((col) => (
                      <Option key={col} value={col}>
                        {col}
                      </Option>
                    ))}
                  </Select>
                </div>

                {targetColumn && (
                  <Button
                    onClick={handleValidate}
                    loading={validating}
                    icon={<CheckCircleOutlined />}
                  >
                    验证数据假设
                  </Button>
                )}

                {validationResult && (
                  <Alert
                    message={validationResult.is_valid ? '验证通过' : '验证警告'}
                    description={
                      <div>
                        <p>
                          数据{validationResult.is_valid ? '满足' : '不完全满足'}
                          时间序列预测的假设条件。
                        </p>
                        {validationResult.recommendations.length > 0 && (
                          <div>
                            <Text strong>建议：</Text>
                            <ul>
                              {validationResult.recommendations.map(
                                (rec: string, idx: number) => (
                                  <li key={idx}>{rec}</li>
                                )
                              )}
                            </ul>
                          </div>
                        )}
                      </div>
                    }
                    type={validationResult.is_valid ? 'success' : 'warning'}
                    showIcon
                  />
                )}

                <div>
                  <Text strong>模型类型（可选）</Text>
                  <Select
                    style={{ width: '100%', marginTop: 8 }}
                    placeholder="留空以自动选择最佳模型"
                    value={modelType}
                    onChange={setModelType}
                    allowClear
                  >
                    <Option value="arima">ARIMA</Option>
                    <Option value="holtwinters">Holt-Winters</Option>
                    <Option value="exponential_smoothing">
                      指数平滑
                    </Option>
                  </Select>
                </div>

                <div>
                  <Text strong>预测周期数</Text>
                  <InputNumber
                    style={{ width: '100%', marginTop: 8 }}
                    min={1}
                    max={100}
                    value={forecastPeriods}
                    onChange={(val) => setForecastPeriods(val || 10)}
                  />
                </div>

                <div>
                  <Text strong>预测需求描述 *</Text>
                  <TextArea
                    style={{ marginTop: 8 }}
                    placeholder="请描述您的预测需求...&#10;例如：预测未来10天的销售趋势，并显示置信区间。"
                    rows={4}
                    value={predictionQuery}
                    onChange={(e) => setPredictionQuery(e.target.value)}
                    maxLength={300}
                    showCount
                  />
                </div>

                <Button
                  type="primary"
                  size="large"
                  icon={<RocketOutlined />}
                  onClick={handlePredict}
                  loading={predicting}
                  disabled={!targetColumn || !predictionQuery.trim()}
                  block
                >
                  {predicting ? '预测中...' : '开始预测'}
                </Button>
              </Space>
            </Card>
          )}

          {/* 预测中 */}
          {predicting && (
            <Card>
              <div style={{ textAlign: 'center', padding: '60px 0' }}>
                <Spin size="large" />
                <Paragraph style={{ marginTop: 24, fontSize: 16 }}>
                  正在执行预测分析，请稍候...
                </Paragraph>
              </div>
            </Card>
          )}

          {/* 预测结果 */}
          {result && (
            <div className="prediction-results">
              <Card
                title="预测结果"
                style={{ marginBottom: 24 }}
                extra={<Button onClick={() => setResult(null)}>重新预测</Button>}
              >
                <Row gutter={[16, 16]}>
                  <Col xs={24} sm={8}>
                    <Statistic
                      title="预测模型"
                      value={result.model_name.toUpperCase()}
                      prefix={<LineChartOutlined />}
                    />
                  </Col>
                  <Col xs={24} sm={8}>
                    <Statistic
                      title="预测点数"
                      value={result.predictions.length}
                    />
                  </Col>
                  <Col xs={24} sm={8}>
                    <Statistic
                      title="验证状态"
                      value={result.validation_passed ? '通过' : '警告'}
                      valueStyle={{
                        color: result.validation_passed ? '#3f8600' : '#cf1322',
                      }}
                      prefix={
                        result.validation_passed ? (
                          <CheckCircleOutlined />
                        ) : (
                          <WarningOutlined />
                        )
                      }
                    />
                  </Col>
                </Row>

                {/* 评估指标 */}
                {Object.keys(result.metrics).length > 0 && (
                  <div style={{ marginTop: 24 }}>
                    <Title level={5}>评估指标</Title>
                    <Row gutter={[16, 16]}>
                      {Object.entries(result.metrics).map(([key, value]) => (
                        <Col xs={24} sm={8} key={key}>
                          <Statistic
                            title={key.toUpperCase()}
                            value={value}
                            precision={4}
                          />
                        </Col>
                      ))}
                    </Row>
                  </div>
                )}
              </Card>

              {/* 预测图表 */}
              <ChartRenderer chart={result.chart} />

              {/* 预测值 */}
              <Card title="预测值" style={{ marginTop: 24 }}>
                <div style={{ maxHeight: 300, overflow: 'auto' }}>
                  {result.predictions.map((pred, idx) => (
                    <Tag key={idx} color="blue" style={{ marginBottom: 8 }}>
                      期数 {idx + 1}: {pred.toFixed(4)}
                    </Tag>
                  ))}
                </div>
              </Card>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default PredictionPage;

