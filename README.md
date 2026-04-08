# 网上商城系统

前后端分离的电商购物平台

## 项目结构

```
djangoProject/
├── backend/                 # Django 后端
│   ├── apps/
│   │   ├── users/          # 用户认证模块
│   │   ├── products/       # 商品管理模块
│   │   ├── cart/           # 购物车模块
│   │   └── orders/         # 订单管理模块
│   ├── djangoProject/      # 项目配置
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── api/           # API 接口
│   │   ├── views/         # 页面组件
│   │   ├── components/    # 公共组件
│   │   ├── stores/        # Pinia 状态管理
│   │   └── router/        # 路由配置
│   ├── package.json
│   └── vite.config.js
│
└── start.bat              # 启动脚本
```

## 技术栈

### 后端
- Django 5.0
- Django REST Framework
- Simple JWT (JWT 认证)
- MySQL

### 前端
- Vue 3
- Vite
- Pinia (状态管理)
- Vue Router
- Element Plus (UI 组件库)
- Axios

## 功能特性

### 用户模块
- [x] 用户注册/登录
- [x] JWT Token 认证
- [x] 个人信息管理
- [x] 修改密码
- [x] 收货地址管理

### 商品模块
- [x] 商品分类
- [x] 商品列表/详情
- [x] 商品搜索/筛选
- [x] 热销/推荐商品
- [x] 商品评价

### 购物车模块
- [x] 添加/删除商品
- [x] 修改数量
- [x] 批量操作
- [x] 购物车统计

### 订单模块
- [x] 创建订单
- [x] 订单列表/详情
- [x] 订单状态管理
- [x] 支付功能 (余额/支付宝/微信)
- [x] 退款申请

## 快速开始

### 1. 安装 MySQL 并创建数据库

```sql
CREATE DATABASE shopping_mall CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

### 4. 使用系统

- 前端: http://localhost:3000
- 后端 API: http://localhost:8000/api/
- API 文档: http://localhost:8000/api/docs/

## API 接口文档

详细 API 文档请访问: http://localhost:8000/api/docs/

### 主要接口

| 模块 | 接口 | 方法 | 说明 |
|------|------|------|------|
| 认证 | /api/users/register/ | POST | 注册 |
| 认证 | /api/users/login/ | POST | 登录 |
| 商品 | /api/products/ | GET | 商品列表 |
| 商品 | /api/products/{id}/ | GET | 商品详情 |
| 购物车 | /api/cart/ | GET/POST | 购物车列表/添加 |
| 订单 | /api/orders/ | POST | 创建订单 |
| 地址 | /api/orders/addresses/ | GET/POST | 地址列表/添加 |

## 管理后台

访问 http://localhost:8000/admin/ 管理商品、订单、用户等数据。

默认需要创建超级用户:
```bash
python manage.py createsuperuser
```
