import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Form, Input, Button, Typography, Space, message } from 'antd';
import {
  UserOutlined,
  LockOutlined,
  MailOutlined,
  RocketOutlined,
} from '@ant-design/icons';
import { registerUser } from '../services/api';
import './LoginPage.css';

const { Title, Paragraph, Text } = Typography;

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [isRegister, setIsRegister] = useState(false);

  const handleLogin = async (values: any) => {
    setLoading(true);
    try {
      // 模拟登录（实际应调用认证API）
      await new Promise((resolve) => setTimeout(resolve, 1000));
      message.success('登录成功！');
      navigate('/');
    } catch (error) {
      message.error('登录失败');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (values: any) => {
    setLoading(true);
    try {
      await registerUser(values.username, values.email);
      message.success('注册成功！请登录');
      setIsRegister(false);
    } catch (error: any) {
      message.error(error.response?.data?.detail || '注册失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-background" />
      <div className="login-container">
        <Card className="login-card">
          <div className="login-header">
            <RocketOutlined className="login-icon" />
            <Title level={2}>数据分析Agent</Title>
            <Paragraph type="secondary">
              智能化数据分析和预测平台
            </Paragraph>
          </div>

          {!isRegister ? (
            // 登录表单
            <Form
              name="login"
              onFinish={handleLogin}
              autoComplete="off"
              size="large"
            >
              <Form.Item
                name="username"
                rules={[{ required: true, message: '请输入用户名！' }]}
              >
                <Input
                  prefix={<UserOutlined />}
                  placeholder="用户名"
                />
              </Form.Item>

              <Form.Item
                name="password"
                rules={[{ required: true, message: '请输入密码！' }]}
              >
                <Input.Password
                  prefix={<LockOutlined />}
                  placeholder="密码"
                />
              </Form.Item>

              <Form.Item>
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={loading}
                  block
                >
                  登录
                </Button>
              </Form.Item>

              <div className="login-footer">
                <Text type="secondary">还没有账号？</Text>
                <Button type="link" onClick={() => setIsRegister(true)}>
                  立即注册
                </Button>
              </div>

              <div className="demo-hint">
                <Text type="secondary" style={{ fontSize: 12 }}>
                  💡 提示：这是演示版本，点击登录即可直接进入系统
                </Text>
              </div>
            </Form>
          ) : (
            // 注册表单
            <Form
              name="register"
              onFinish={handleRegister}
              autoComplete="off"
              size="large"
            >
              <Form.Item
                name="username"
                rules={[
                  { required: true, message: '请输入用户名！' },
                  { min: 3, message: '用户名至少3个字符！' },
                ]}
              >
                <Input
                  prefix={<UserOutlined />}
                  placeholder="用户名"
                />
              </Form.Item>

              <Form.Item
                name="email"
                rules={[
                  { type: 'email', message: '请输入有效的邮箱地址！' },
                ]}
              >
                <Input
                  prefix={<MailOutlined />}
                  placeholder="邮箱（可选）"
                />
              </Form.Item>

              <Form.Item
                name="password"
                rules={[
                  { required: true, message: '请输入密码！' },
                  { min: 6, message: '密码至少6个字符！' },
                ]}
              >
                <Input.Password
                  prefix={<LockOutlined />}
                  placeholder="密码"
                />
              </Form.Item>

              <Form.Item
                name="confirm"
                dependencies={['password']}
                rules={[
                  { required: true, message: '请确认密码！' },
                  ({ getFieldValue }) => ({
                    validator(_, value) {
                      if (!value || getFieldValue('password') === value) {
                        return Promise.resolve();
                      }
                      return Promise.reject(new Error('两次密码不一致！'));
                    },
                  }),
                ]}
              >
                <Input.Password
                  prefix={<LockOutlined />}
                  placeholder="确认密码"
                />
              </Form.Item>

              <Form.Item>
                <Button
                  type="primary"
                  htmlType="submit"
                  loading={loading}
                  block
                >
                  注册
                </Button>
              </Form.Item>

              <div className="login-footer">
                <Text type="secondary">已有账号？</Text>
                <Button type="link" onClick={() => setIsRegister(false)}>
                  立即登录
                </Button>
              </div>
            </Form>
          )}
        </Card>

        {/* 功能介绍 */}
        <div className="features-showcase">
          <Space direction="vertical" size="large">
            <Card className="feature-showcase-card">
              <Space>
                <RocketOutlined style={{ fontSize: 32, color: '#1890ff' }} />
                <div>
                  <Text strong>AI驱动</Text>
                  <br />
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    智能分析，自然语言交互
                  </Text>
                </div>
              </Space>
            </Card>
            <Card className="feature-showcase-card">
              <Space>
                <UserOutlined style={{ fontSize: 32, color: '#52c41a' }} />
                <div>
                  <Text strong>简单易用</Text>
                  <br />
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    无需编程，开箱即用
                  </Text>
                </div>
              </Space>
            </Card>
          </Space>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;

