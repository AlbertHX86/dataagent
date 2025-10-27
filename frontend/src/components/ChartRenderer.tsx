import React from 'react';
import Plot from 'react-plotly.js';
import { Card, Empty } from 'antd';
import { ChartConfig } from '../services/api';

interface ChartRendererProps {
  chart: ChartConfig;
}

const ChartRenderer: React.FC<ChartRendererProps> = ({ chart }) => {
  if (!chart || !chart.data) {
    return (
      <Card>
        <Empty description="暂无图表数据" />
      </Card>
    );
  }

  try {
    // Plotly图表
    return (
      <Card title={chart.title} style={{ marginBottom: 16 }}>
        <Plot
          data={chart.data.data}
          layout={{
            ...chart.data.layout,
            autosize: true,
            height: 400,
            margin: { t: 40, r: 40, b: 40, l: 60 },
          }}
          config={{
            displayModeBar: true,
            displaylogo: false,
            responsive: true,
          }}
          style={{ width: '100%' }}
        />
      </Card>
    );
  } catch (error) {
    console.error('Chart rendering error:', error);
    return (
      <Card title={chart.title}>
        <Empty description="图表渲染失败" />
      </Card>
    );
  }
};

export default ChartRenderer;

