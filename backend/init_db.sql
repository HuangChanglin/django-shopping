-- 创建数据库
CREATE DATABASE IF NOT EXISTS shopping_mall CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE shopping_mall;

-- 执行迁移后会创建以下表:
-- users (用户表)
-- categories (商品分类表)
-- products (商品表)
-- product_images (商品图片表)
-- reviews (商品评价表)
-- cart_items (购物车表)
-- orders (订单表)
-- order_items (订单商品表)
-- addresses (收货地址表)
