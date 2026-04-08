from django.db import models


class Category(models.Model):
    name = models.CharField('分类名称', max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    sort = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'categories'
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name
        ordering = ['sort', '-id']

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('active', '上架'),
        ('offline', '下架'),
    ]
    
    name = models.CharField('商品名称', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    description = models.TextField('商品描述', blank=True)
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    original_price = models.DecimalField('原价', max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField('库存', default=0)
    sales = models.IntegerField('销量', default=0)
    images = models.JSONField('商品图片', default=list)
    specs = models.JSONField('规格属性', default=dict)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='draft')
    is_hot = models.BooleanField('热销', default=False)
    is_recommended = models.BooleanField('推荐', default=False)
    weight = models.DecimalField('重量(kg)', max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = '商品'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def discount_rate(self):
        if self.original_price and self.original_price > 0:
            return round((1 - self.price / self.original_price) * 100)
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField('图片', upload_to='products/')
    sort = models.IntegerField('排序', default=0)
    is_main = models.BooleanField('主图', default=False)

    class Meta:
        db_table = 'product_images'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name
        ordering = ['sort']


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField('评分', choices=[(i, i) for i in range(1, 6)])
    content = models.TextField('评价内容')
    images = models.JSONField('评价图片', default=list)
    is_anonymous = models.BooleanField('匿名评价', default=False)
    created_at = models.DateTimeField('评价时间', auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        verbose_name = '商品评价'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
