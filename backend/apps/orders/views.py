from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from django.utils import timezone
from .models import Order, OrderItem, Address
from .serializers import (
    OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer,
    AddressSerializer, PaymentSerializer, ExpressSerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Order.objects.all()
            status_filter = self.request.query_params.get('status')
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            return queryset
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order.status = serializer.validated_data['status']
        order.save()
        
        return Response({'message': '状态更新成功', 'status': order.status})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def ship(self, request, pk=None):
        order = self.get_object()
        serializer = ExpressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order.status = 'shipped'
        order.express_company = serializer.validated_data['express_company']
        order.express_no = serializer.validated_data['express_no']
        order.save()
        
        return Response({'message': '订单已发货'})

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        order = self.get_object()
        
        if order.status != 'pending':
            return Response({'message': '订单状态不允许支付'}, status=status.HTTP_400_BAD_REQUEST)
        
        payment_method = request.data.get('payment_method', 'balance')
        
        if payment_method == 'balance':
            if request.user.balance < order.actual_amount:
                return Response({'message': '余额不足'}, status=status.HTTP_400_BAD_REQUEST)
            
            from django.contrib.auth import get_user_model
            User = get_user_model()
            User.objects.filter(pk=request.user.pk).update(
                balance=request.user.balance - order.actual_amount
            )
        
        order.status = 'paid'
        order.payment_method = payment_method
        order.payment_no = f"{payment_method}_{timezone.now().strftime('%Y%m%d%H%M%S')}"
        order.paid_at = timezone.now()
        order.save()
        
        return Response({'message': '支付成功'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        
        if order.status not in ['pending', 'paid']:
            return Response({'message': '订单状态不允许取消'}, status=status.HTTP_400_BAD_REQUEST)
        
        if order.status == 'paid' and order.payment_method == 'balance':
            from django.contrib.auth import get_user_model
            User = get_user_model()
            User.objects.filter(pk=request.user.pk).update(
                balance=request.user.balance + order.actual_amount
            )
        
        order.status = 'cancelled'
        order.save()
        
        return Response({'message': '订单已取消'})

    @action(detail=True, methods=['post'])
    def confirm_receive(self, request, pk=None):
        order = self.get_object()
        
        if order.status != 'shipped':
            return Response({'message': '订单状态不允许确认收货'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'delivered'
        order.save()
        
        return Response({'message': '已确认收货'})

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        order = self.get_object()
        
        if order.status not in ['paid', 'shipped', 'delivered']:
            return Response({'message': '订单状态不允许退款'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'refunding'
        order.save()
        
        return Response({'message': '退款申请已提交'})

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        user = request.user
        queryset = Order.objects.filter(user=user)
        
        total_orders = queryset.count()
        pending_orders = queryset.filter(status='pending').count()
        completed_orders = queryset.filter(status='completed').count()
        total_spent = queryset.filter(status__in=['paid', 'shipped', 'delivered', 'completed']).aggregate(
            total=models.Sum('actual_amount')
        )['total'] or 0
        
        return Response({
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'completed_orders': completed_orders,
            'total_spent': total_spent
        })


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def set_default(self, request):
        address_id = request.data.get('address_id')
        try:
            address = Address.objects.get(id=address_id, user=request.user)
            address.is_default = True
            address.save()
            return Response({'message': '已设为默认地址'})
        except Address.DoesNotExist:
            return Response({'message': '地址不存在'}, status=status.HTTP_404_NOT_FOUND)
