from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product

User = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('shipped', '已发货'),
        ('delivered', '已收货'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
        ('refunding', '退款中'),
        ('refunded', '已退款'),
    ]
    
    PAYMENT_METHODS = [
        ('alipay', '支付宝'),
        ('wechat', '微信支付'),
        ('balance', '余额支付'),
    ]

    order_no = models.CharField('订单号', max_length=32, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    total_amount = models.DecimalField('订单总额', max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField('优惠金额', max_digits=10, decimal_places=2, default=0)
    freight_amount = models.DecimalField('运费', max_digits=10, decimal_places=2, default=0)
    actual_amount = models.DecimalField('实付金额', max_digits=10, decimal_places=2)
    
    receiver_name = models.CharField('收货人', max_length=50)
    receiver_phone = models.CharField('联系电话', max_length=11)
    receiver_address = models.TextField('收货地址')
    
    payment_method = models.CharField('支付方式', max_length=20, choices=PAYMENT_METHODS)
    payment_no = models.CharField('支付流水号', max_length=64, blank=True)
    paid_at = models.DateTimeField('支付时间', null=True, blank=True)
    
    status = models.CharField('订单状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    remark = models.TextField('备注', blank=True)
    
    express_company = models.CharField('快递公司', max_length=50, blank=True)
    express_no = models.CharField('快递单号', max_length=50, blank=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'orders'
        verbose_name = '订单'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.order_no


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField('商品名称', max_length=200)
    product_image = models.CharField('商品图片', max_length=500)
    price = models.DecimalField('单价', max_digits=10, decimal_places=2)
    quantity = models.IntegerField('数量')
    specs = models.JSONField('规格', default=dict)

    @property
    def subtotal(self):
        return self.price * self.quantity

    class Meta:
        db_table = 'order_items'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField('收货人', max_length=50)
    phone = models.CharField('联系电话', max_length=11)
    province = models.CharField('省份', max_length=50)
    city = models.CharField('城市', max_length=50)
    district = models.CharField('区县', max_length=50)
    address = models.TextField('详细地址')
    is_default = models.BooleanField('默认地址', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'addresses'
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.province} {self.city} {self.district} {self.address}"

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
