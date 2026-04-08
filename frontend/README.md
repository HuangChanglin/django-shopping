# 网上商城系统 - Vue 3 前端优化版

前后端分离的电商购物平台，基于 Vue 3 Composition API 构建。

## 优化亮点

### 1. 组件优化
- **ProductCard**: 商品卡片组件，支持动画、悬停效果、快捷操作
- **SkeletonLoader**: 骨架屏组件，支持多种加载状态
- **ScrollToTop**: 滚动回到顶部组件，带平滑动画

### 2. Composables (可复用逻辑)
- `usePagination`: 分页逻辑封装
- `useSearch`: 搜索功能封装，支持防抖
- `useSelection`: 多选功能封装
- `useCountdown`: 倒计时功能
- `useScrollToTop`: 滚动相关功能

### 3. UI/UX 优化
- 页面切换过渡动画
- 列表项入场动画
- 骨架屏加载状态
- 平滑滚动效果
- 渐变背景和粒子效果
- 响应式设计

### 4. 最佳实践
- Vue 3 Composition API
- Script Setup 语法糖
- Pinia 状态管理
- 路由懒加载
- 错误边界处理

## 项目结构

```
frontend/
├── src/
│   ├── api/              # API 接口
│   ├── assets/          # 静态资源
│   ├── components/      # 公共组件
│   │   ├── ProductCard.vue     # 商品卡片
│   │   ├── SkeletonLoader.vue  # 骨架屏
│   │   └── ScrollToTop.vue     # 回到顶部
│   ├── composables/      # 组合式函数
│   │   ├── useCommon.js        # 通用逻辑
│   │   ├── useUtils.js         # 工具函数
│   │   └── useScroll.js        # 滚动相关
│   ├── stores/          # Pinia 状态
│   ├── utils/           # 工具函数
│   ├── views/           # 页面组件
│   ├── router/          # 路由配置
│   └── main.js          # 入口文件
└── package.json
```

## 功能模块

| 模块 | 功能 |
|------|------|
| 首页 | Banner 轮播、热门推荐、商品展示 |
| 商品 | 分类筛选、搜索、分页、详情页 |
| 购物车 | 多选操作、数量调整、批量删除 |
| 订单 | 创建订单、支付、状态管理 |
| 用户 | 登录注册、个人中心、地址管理 |

## 启动前端

```bash
cd frontend
npm install
npm run dev
```

## 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Pinia** - Vue 状态管理
- **Vue Router** - Vue 官方路由
- **Element Plus** - Vue 3 UI 组件库
- **Axios** - HTTP 客户端
- **Sass** - CSS 预处理器
