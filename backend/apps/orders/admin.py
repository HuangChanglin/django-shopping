from django.contrib import admin
from .models import Order, OrderItem, Address


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'product_image', 'price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'user', 'actual_amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_no', 'user__username', 'receiver_phone']
    readonly_fields = ['order_no', 'total_amount', 'discount_amount', 'freight_amount', 'actual_amount']
    inlines = [OrderItemInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'phone', 'province', 'city', 'is_default']
    list_filter = ['is_default', 'province', 'city']
    search_fields = ['user__username', 'name', 'phone']
