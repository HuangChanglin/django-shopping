from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product

User = get_user_model()


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField('数量', default=1)
    selected_specs = models.JSONField('选中的规格', default=dict)
    created_at = models.DateTimeField('添加时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'cart_items'
        verbose_name = '购物车商品'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'product', 'selected_specs']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity
