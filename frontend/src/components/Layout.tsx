import React, { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  Layout as AntLayout,
  Menu,
  Button,
  Avatar,
  Dropdown,
  Space,
} from 'antd';
import {
  HomeOutlined,
  BarChartOutlined,
  LineChartOutlined,
  FolderOutlined,
  UserOutlined,
  LogoutOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';
import './Layout.css';

const { Header, Sider, Content } = AntLayout;

const Layout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);

  // 获取当前选中的菜单项
  const getSelectedKey = () => {
    const path = location.pathname;
    if (path === '/') return '1';
    if (path.startsWith('/analysis')) return '2';
    if (path.startsWith('/prediction')) return '3';
    if (path.startsWith('/workspace')) return '4';
    return '1';
  };

  // 菜单项
  const menuItems: MenuProps['items'] = [
    {
      key: '1',
      icon: <HomeOutlined />,
      label: '首页',
      onClick: () => navigate('/'),
    },
    {
      key: '2',
      icon: <BarChartOutlined />,
      label: '数据分析',
      onClick: () => navigate('/analysis'),
    },
    {
      key: '3',
      icon: <LineChartOutlined />,
      label: '预测分析',
      onClick: () => navigate('/prediction'),
    },
    {
      key: '4',
      icon: <FolderOutlined />,
      label: '我的工作',
      onClick: () => navigate('/workspace'),
    },
  ];

  // 用户菜单
  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '个人信息',
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录',
      onClick: () => navigate('/login'),
    },
  ];

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Header className="layout-header">
        <div className="logo">
          <BarChartOutlined style={{ fontSize: 24, marginRight: 12 }} />
          <span>数据分析Agent</span>
        </div>
        <div className="header-right">
          <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
            <Space style={{ cursor: 'pointer' }}>
              <Avatar icon={<UserOutlined />} />
              <span style={{ color: '#fff' }}>演示用户</span>
            </Space>
          </Dropdown>
        </div>
      </Header>
      <AntLayout>
        <Sider
          collapsible
          collapsed={collapsed}
          onCollapse={setCollapsed}
          theme="light"
          width={220}
        >
          <Menu
            mode="inline"
            selectedKeys={[getSelectedKey()]}
            items={menuItems}
            style={{ height: '100%', borderRight: 0 }}
          />
        </Sider>
        <Content className="layout-content">
          <div className="content-wrapper">
            <Outlet />
          </div>
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

export default Layout;

