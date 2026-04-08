from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from .models import Order, OrderItem, Address
from apps.cart.models import CartItem


class AddressSerializer(serializers.ModelSerializer):
    full_address = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ['id', 'name', 'phone', 'province', 'city', 'district', 'address', 'full_address', 'is_default']
        read_only_fields = ['id']

    def get_full_address(self, obj):
        return f"{obj.province} {obj.city} {obj.district} {obj.address}"


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'price', 'quantity', 'specs', 'subtotal']
        read_only_fields = ['id', 'product_name', 'product_image', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_no', 'total_amount', 'discount_amount', 'freight_amount',
            'actual_amount', 'receiver_name', 'receiver_phone', 'receiver_address',
            'payment_method', 'status', 'express_company', 'express_no',
            'remark', 'created_at', 'paid_at', 'items'
        ]
        read_only_fields = [
            'id', 'order_no', 'total_amount', 'discount_amount', 'freight_amount',
            'actual_amount', 'created_at', 'paid_at'
        ]


class OrderCreateSerializer(serializers.Serializer):
    address_id = serializers.IntegerField(required=False)
    receiver_name = serializers.CharField(max_length=50, required=False)
    receiver_phone = serializers.CharField(max_length=11, required=False)
    receiver_address = serializers.CharField(required=False)
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_METHODS)
    remark = serializers.CharField(required=False, allow_blank=True)
    cart_item_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text='从购物车选择的商品ID'
    )

    def validate(self, attrs):
        user = self.context['request'].user
        
        if attrs.get('address_id'):
            try:
                address = Address.objects.get(id=attrs['address_id'], user=user)
                attrs['receiver_name'] = address.name
                attrs['receiver_phone'] = address.phone
                attrs['receiver_address'] = f"{address.province} {address.city} {address.district} {address.address}"
            except Address.DoesNotExist:
                raise serializers.ValidationError({'address_id': '地址不存在'})
        else:
            if not all([attrs.get('receiver_name'), attrs.get('receiver_phone'), attrs.get('receiver_address')]):
                raise serializers.ValidationError('请提供地址信息')
        
        cart_item_ids = attrs.get('cart_item_ids')
        if cart_item_ids:
            cart_items = CartItem.objects.filter(id__in=cart_item_ids, user=user)
            if cart_items.count() != len(cart_item_ids):
                raise serializers.ValidationError({'cart_item_ids': '部分商品不存在或不属于您'})
        else:
            cart_items = CartItem.objects.filter(user=user)
        
        attrs['cart_items'] = list(cart_items)
        if not cart_items:
            raise serializers.ValidationError({'cart_item_ids': '购物车为空'})
        
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        cart_items = validated_data.pop('cart_items')
        validated_data.pop('address_id', None)
        
        import uuid
        order_no = f"{timezone.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8].upper()}"
        
        total_amount = sum(item.subtotal for item in cart_items)
        freight_amount = 10 if total_amount < 99 else 0
        
        order = Order.objects.create(
            order_no=order_no,
            user=user,
            total_amount=total_amount,
            freight_amount=freight_amount,
            actual_amount=total_amount + freight_amount,
            **validated_data
        )
        
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                product_image=cart_item.product.images[0] if cart_item.product.images else '',
                price=cart_item.product.price,
                quantity=cart_item.quantity,
                specs=cart_item.selected_specs
            )
        
        cart_items.delete()
        
        return order


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)


class PaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_METHODS)


class ExpressSerializer(serializers.Serializer):
    express_company = serializers.CharField(max_length=50)
    express_no = serializers.CharField(max_length=50)
